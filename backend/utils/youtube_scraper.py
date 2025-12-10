"""
Utilidad para extraer comentarios de YouTube usando YouTube Data API v3.
"""

import re
import os
from typing import List, Dict, Optional
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class YouTubeCommentFetcher:
    """Extrae comentarios de videos de YouTube usando YouTube Data API v3."""
    
    def __init__(self):
        """Inicializa el cliente de YouTube Data API."""
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            logger.warning("YOUTUBE_API_KEY no configurada. El servicio no funcionará.")
        else:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                logger.info("YouTube Data API inicializada correctamente")
            except Exception as e:
                logger.error(f"Error al inicializar YouTube API: {str(e)}")
                self.youtube = None
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extrae el video ID de una URL de YouTube.
        
        Args:
            url: URL de YouTube (youtube.com/watch?v= o youtu.be/)
            
        Returns:
            str: Video ID o None si no es válida
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
            r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        ]        
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Valida si una URL es de Youtube."""
        return YouTubeCommentFetcher.extract_video_id(url) is not None
    
    def fetch_comments(self, video_id: str, max_comments: int = 200) -> List[Dict]:
        """
        Extrae comentarios de un video de YouTube usando YouTube Data API v3.
        
        Args:
            video_id: ID del video de YouTube
            max_comments: Número máximo de comentarios a extraer (1-200, default: 200)
            
        Returns:
            Lista de diccionarios con los comentarios
            
        Raises:
            ValueError: Si no hay API key configurada o video no disponible
            HttpError: Si hay error en la API de YouTube
        """
        if not self.api_key or not self.youtube:
            raise ValueError("YOUTUBE_API_KEY no configurada. Configura la variable de entorno.")
        
        try:
            logger.info(f"Extrayendo hasta {max_comments} comentarios del video {video_id}")
            
            # Llamada a la API para obtener comentarios
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(max_comments, 100),  # API permite máximo 100 por request
                order="relevance",  # Comentarios más relevantes primero
                textFormat="plainText"
            )
            
            response = request.execute()
            comments = []
            
            # Procesar comentarios de la respuesta
            for item in response.get('items', []):
                snippet = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'comment_id': item['snippet']['topLevelComment']['id'],
                    'author': snippet.get('authorDisplayName', 'Unknown'),
                    'text': snippet.get('textDisplay', ''),
                    'published_at': snippet.get('publishedAt', '')
                })
            
            # Si necesitamos más comentarios y hay más páginas disponibles
            while len(comments) < max_comments and 'nextPageToken' in response:
                request = self.youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=min(max_comments - len(comments), 100),
                    pageToken=response['nextPageToken'],
                    order="relevance",
                    textFormat="plainText"
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    if len(comments) >= max_comments:
                        break
                    snippet = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'comment_id': item['snippet']['topLevelComment']['id'],
                        'author': snippet.get('authorDisplayName', 'Unknown'),
                        'text': snippet.get('textDisplay', ''),
                        'published_at': snippet.get('publishedAt', '')
                    })
            
            logger.info(f"Extraídos {len(comments)} comentarios del video {video_id}")
            return comments
            
        except HttpError as e:
            error_reason = e.error_details[0]['reason'] if e.error_details else 'unknown'
            
            if error_reason == 'videoNotFound':
                raise ValueError("Video no encontrado")
            elif error_reason == 'commentsDisabled':
                logger.warning(f"Comentarios deshabilitados para el video {video_id}")
                return []
            elif error_reason == 'forbidden':
                raise ValueError("Video privado o restringido")
            else:
                logger.error(f"Error de YouTube API: {str(e)}")
                raise ValueError(f"Error al acceder al video: {error_reason}")
        
        except Exception as e:
            logger.error(f"Error inesperado extrayendo comentarios: {str(e)}")
            raise
        
    def fetch_video_title(self, video_id: str) -> str:
        """
        Obtiene el título de un video de YouTube.
        
        Args:
            video_id: ID del video de YouTube
            
        Returns:
            Título del video o fallback si hay error
        """
        if not self.api_key or not self.youtube:
            logger.warning("No se puede obtener titulo: YOUTUBE_API_KEY no configurada")       
            return f"Video {video_id}" 
        
        try: 
            request = self.youtube.videos().list(
                part="snippet",
                id=video_id
            )
            
            response = request.execute()
            
            if response.get('items'):
                return response['items'][0]['snippet']['title']
            else:
                logger.warning(f"No se encontró informacion del video {video_id}")
                return f"Video {video_id}"
            
        except HttpError as e:
            logger.error(f"Error obteniendo titulo del video {video_id}: {str(e)}")
            return f"Video {video_id}"
        except Exception as e: 
            logger.error(f"Error inesperado obteniendo titulo: {str(e)}")
            return f"Video {video_id}"
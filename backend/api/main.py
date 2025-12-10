"""
API REST para detección de hate speech en comentarios de YouTube.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.models.model_loader import HateSpeechDetector, DistilBERTDetector
from datetime import datetime
from backend.utils.youtube_scraper import YouTubeCommentFetcher
import logging
from fastapi.middleware.cors import CORSMiddleware


#Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Inicializar FastAPI
app = FastAPI(
    title="YouTube Hate Speech Detector API",
    description="API para detectar mensajes de odio en comentarios de YouTube",
    version="1.0.0"
)

#Cargar modelos al inicio (singleton)
detector = None
bert_detector = None
youtube_fetcher = None

@app.on_event("startup")
async def load_model():
    """Carga los modelos al iniciar la aplicación."""
    global detector, bert_detector, youtube_fetcher
    try:
        detector = HateSpeechDetector()
        logger.info("✅ Modelo Logistic Regression cargado exitosamente")
        
        bert_detector = DistilBERTDetector()
        logger.info("✅ Modelo DistilBERT cargado exitosamente")
        
        youtube_fetcher = YouTubeCommentFetcher()
        logger.info("✅ YouTube Comment Fetcher inicializado")
    except Exception as e:
        logger.error(f"❌ Error cargando modelos: {e}")
        raise


# === MODELOS PYDANTIC ===

class TextInput(BaseModel):
    """Modelo para input de predicción individual."""
    text: str = Field(..., min_lenght=1, max_lenght=5000, description="Texto del comentario a analizar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I hate you, you're so stupid!"
            }
        }
class BatchTextInput(BaseModel):
    """Modelo para input de predicción por lotes."""
    texts: List[str] = Field(..., min_items=1, max_items=100, description="Lista de comentarios a analizar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "texts": [
                    "I love this video!",
                    "You're an idiot!",
                    "Thanks for sharing"
                ]
            }
        }

class PredictionOutput(BaseModel):
    """Modelo para output de predicción."""
    text: str
    prediction: str
    confidence: float
    is_toxic: bool
    threshold_used: float

class BatchPredictionOutput(BaseModel):
    """Modelo para output de predicción por lotes."""
    results: List[PredictionOutput]
    total: int


class HealthResponse(BaseModel):
    """Modelo para health check."""
    status: str
    service: str
    models: dict
    

class ModelInfoResponse(BaseModel):
    """Modelo para información del modelo."""
    model_type: str
    threshold: float
    vectorizer_type: str
    vocab_size: int
    model_loaded: bool
    vectorizer_loaded: bool

# ==================== YouTube Analysis Models ====================

class YouTubeURLInput(BaseModel):
    """Modelo para input de análisis de Youtube."""
    url: str = Field(
        ...,
        description="URL del video de Youtube",
        pattern=r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}"
    )
    max_comments: Optional[int] = Field(
        200,
        ge=1,
        le=200,
        description="Número máximo de comentarios a analizar"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "max_comments": 100
            }
        }

class CommentAnalysis(BaseModel):
    """Analisis individual de un comentario."""
    comment_id: str
    author: str
    text: str
    prediction: str # 'hate_speech' | 'normal'
    confidence: float
    is_toxic: bool
    published_at: str

class YouTubeAnalysisOutput(BaseModel):
    """Resultado completo del análisis de video."""
    video_id: str
    video_title: str
    total_comments_analyzed: int
    toxic_count: int
    normal_count: int
    toxicity_percentage: float
    top_toxic_comments: List[CommentAnalysis] = Field(
        ...,
        description="Top 10 comentarios mas toxicos ordenados por confidence"
    )
    analysis_timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "video_id": "dQw4w9WgXcQ",
                "video_title": "Rick Astley - Never Gonna Give You Up",
                "total_comments_analyzed": 150,
                "toxic_count": 23,
                "normal_count": 127,
                "toxicity_percentage": 15.33,
                "top_toxic_comments": [],
                "analysis_timestamp": "2025-12-05T10:30:00"
            }
        }


# === ENDPOINTS ===    

@app.get("/", tags=["General"])
async def root():
    """Endpoint raíz de la API."""
    return {
        "message": "Youtube Hate Speech Detector API",
        "version": "1.0.0",
        "models": {
            "logistic_regression": "Modelo clásico optimizado (Threshold 0.3)",
            "distilbert": "Transformer fine-tuned (88% accuracy)"
        },
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict (LR)",
            "predict_transformer": "/predict/transformer (DistilBERT)",
            "predict_compare": "/predict/compare (LR vs BERT)",
            "predict_batch": "/predict/batch",
            "model_info": "/model/info"
        }
    }
 
@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """
    Verifica el estado de la API y del modelo.
    
    Returns:
        HealthResponse: Estado de salud del servicio
    """
    lr_loaded = detector is not None and detector.model is not None
    bert_loaded = bert_detector is not None and bert_detector.model is not None
    
    return HealthResponse(
        status="healthy" if (lr_loaded and bert_loaded) else "degraded",
        service="hate-speech-detector",
        models= {
            "logistic_regression": {
                "loaded": lr_loaded,
                "type": "Logistic Regression",
                "threshold": 0.3
            },
            "distilbert": {
                "loaded": bert_loaded,
                "type": "DistilBERT-base-uncased",
                "parameters": "66M"
            }
        }
    )

@app.post("/predict", response_model=PredictionOutput, tags=["Predictions"])
async def predict(input_data: TextInput):
    """
    Predice si un comentario contiene hate speech.
    
    Args:
        input_data: Objeto con el texto a analizar
        
    Returns:
        PredictionOutput: Predicción con confianza y metadatos
        
    Raises:
        HTTPException: Si el modelo no está cargado o hay error en la predicción
    """
    if detector is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        result = detector.predict(input_data.text)
        return PredictionOutput(**result)
    
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")
    

@app.post("/predict/batch", response_model=BatchPredictionOutput, tags=["Predictions"])
async def predict_batch(input_data: BatchTextInput):
    """
    Predice múltiples comentarios de una vez (más eficiente que llamadas individuales).
    
    Args:
        input_data: Objeto con lista de textos a analizar
        
    Returns:
        BatchPredictionOutput: Lista de predicciones
        
    Raises:
        HTTPException: Si el modelo no está cargado o hay error
    """
    if detector is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        results = detector.predict_batch(input_data.texts)
        return BatchPredictionOutput(
            results=[PredictionOutput(**r) for r in results],
            total=len(results)
        )
    
    except Exception as e:
        logger.error(f"Error en predicción batch: {e}")
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")
    

@app.get("/model/info", response_model=ModelInfoResponse, tags=["Model"])
async def get_model_info():
    """
    Retorna información sobre el modelo Logistic Regression.
    
    Returns:
        ModelInfoResponse: Información del modelo
        
    Raises:
        HTTPException: Si el modelo no está cargado
    """
    if detector is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        info = detector.get_model_info()
        return ModelInfoResponse(**info)
    
    except Exception as e:
        logger.error(f"Error obteniendo info del modelo: {e}")
        raise HTTPException(status_code=500, detail=f"Error:{str(e)}")
    
@app.post("/predict/transformer", response_model=PredictionOutput, tags=["Predictions"])
async def predict_transformer(input_data: TextInput):
    """
    Predice si un comentario contiene hate speech usando DistilBERT.
    
    Ventajas sobre LR:
    - Mayor accuracy (88% vs 52%)
    - Mejor F1-score (87% vs 66%)
    - Menor overfitting (3.3% vs 23%)
    
    Args:
        input_data: Objeto con el texto a analizar
        
    Returns:
        PredictionOutput: Predicción con confianza y probabilidades
    """
    if bert_detector is None:
        raise HTTPException(status_code=503, detail="Modelo DistilBERT no disponible")    
    try: 
        result = bert_detector.predict(input_data.text)
        
        # Adaptar formato para PredictionOutput
        return PredictionOutput(
            text=result['text'],
            prediction=result['prediction'],
            confidence=result['confidence'],
            is_toxic=result['label'] == 1, 
            threshold_used=0.5      # DistilBERT usa softmax, threshold implicito 0.5
        )
        
    except Exception as e:
        logger.error(f"Error en prediccion DistilBERT: {e}")
        raise HTTPException(status_code=500, detail=f"Error en prediccion: {str(e)}")

@app.post("/predict/compare", tags=["Predictions"])
async def predict_compare(input_data: TextInput):
    """
    Compara predicciones de Logistic Regression vs DistilBERT.
    
    Útil para:
    - Ver diferencias de confianza entre modelos
    - Identificar casos donde los modelos no están de acuerdo
    - Debugging y análisis de errores
    
    Args:
        input_data: Objeto con el texto a analizar
        
    Returns:
        dict: Predicciones de ambos modelos + métricas de comparación
    """
    if detector is None or bert_detector is None:
        raise HTTPException (status_code=503, details="Modelos no disponibles")
    
    try:
        # Predicciones de ambos modelos
        lr_result = detector.predict(input_data.text)
        bert_result = bert_detector.predict(input_data.text)
        
        # Formatear respuesta comparativa
        return {
            "text": input_data.text,
            "logistic_regression": {
                "prediction": lr_result['prediction'],
                "confidence": lr_result['confidence'],
                "is_toxic": lr_result['is_toxic'],
                "threshold": lr_result['threshold_used']
            },
            "distilbert": {
                "prediction": bert_result['prediction'],
                "confidence": bert_result['confidence'],
                "probabilities": bert_result['probabilities']
            },
            "comparison": {
                "agreement": lr_result['prediction'] == bert_result['prediction'],
                "confidence_diff": abs(lr_result['confidence'] - bert_result['confidence']),
                "both_confident": lr_result['confidence'] > 0.7 and bert_result['confidence'] > 0.7,
                "recommended_model": "distilbert" if bert_result['confidence'] > lr_result['confidence'] else "logistic_regression"
            }
        }
    
    except Exception as e:
        logger.error(f"Error en comparación: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



# ==================== YOUTUBE ANALYSIS ENDPOINT ====================

@app.post("/analyze/video", response_model=YouTubeAnalysisOutput, tags=["YouTube Analysis"])
async def analyze_youtube_video(input_data: YouTubeURLInput):
    """
    Analiza los comentarios de un video de YouTube para detectar hate speech.
    
    Extrae hasta 200 comentarios del video y los analiza usando DistilBERT.
    Retorna estadísticas de toxicidad y los top 10 comentarios más tóxicos.
    
    Args:
        input_data: URL del video y número máximo de comentarios
        
    Returns:
        YouTubeAnalysisOutput: Análisis completo con estadísticas y top comentarios tóxicos
        
    Raises:
        HTTPException 400: URL inválida
        HTTPException 404: Video no encontrado, privado o sin comentarios accesibles
        HTTPException 503: Modelo DistilBERT no disponible
        HTTPException 500: Error interno durante el análisis
    """
    # Verificar que el modelo esté disponible
    if bert_detector is None:
        raise HTTPException(
            status_code=503,
            detail="Modelo DistilBERT no disponible"
        )
    
    if youtube_fetcher is None:
        raise HTTPException(
            status_code=503,
            detail="YouTube Comment Fetcher no inicializado"
        )
    
    try:
        # Validar URL
        if not youtube_fetcher.validate_url(input_data.url):
            raise HTTPException(
                status_code=400,
                detail="URL de YouTube inválida. Use formato: youtube.com/watch?v=XXX o youtu.be/XXX"
            )
        
        # Extraer video ID
        video_id = youtube_fetcher.extract_video_id(input_data.url)
        if not video_id:
            raise HTTPException(
                status_code=400,
                detail="No se pudo extraer el ID del video de la URL"
            )                
            
        logger.info(f"Analizando video {video_id}, max_comments={input_data.max_comments}")

        # Obtener título del video
        video_title = youtube_fetcher.fetch_video_title(video_id)
        
        # Extraer comentarios con timeout
        try:
            comments = youtube_fetcher.fetch_comments(
                video_id=video_id,
                max_comments=input_data.max_comments
            )
        
        except ValueError as e:
            raise HTTPException(
                status_code=404,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error extrayendo comentarios: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al extraer comentarios: {str(e)}"
            )
            
        # Caso: video sin comentarios
        if not comments or len(comments) == 0:
            logger.warning(f"Video {video_id} no tiene comentarios disponibles")
            return YouTubeAnalysisOutput(
                video_id=video_id,
                video_title="Video sin comentarios disponibles",
                total_comments_analyzed=0,
                toxic_count=0,
                normal_count=0,
                toxicity_percentage=0.0,
                top_toxic_comments=[],
                analysis_timestamp=datetime.now().isoformat()
            )
            
        # Extraer solo los textos para batch prediction
        texts = [comment['text'] for comment in comments if comment.get('text')]
        
        if not texts:
            logger.warning(f"No se encontraron textos validos en los comentarios")
            return YouTubeAnalysisOutput(
                video_id=video_id,
                video_title="Sin textos válidos",
                total_comments_analyzed=0,
                toxic_count=0,
                normal_count=0,
                toxicity_percentage=0.0,
                top_toxic_comments=[],
                analysis_timestamp=datetime.now().isoformat()
            )
        
        logger.info(f"Analizando {len(texts)} comentarios con DistilBERT...")
        
        # Prediccion en batch (mas eficiente)
        predictions = bert_detector.predict_batch(texts)
        
        # Combinar predicciones con metadata de comentarios
        analyzed_comments = []
        toxic_count = 0
        normal_count = 0
        
        for i, (comment, prediction) in enumerate(zip(comments[:len(predictions)], predictions)):
            is_toxic = prediction['prediction'] == 'hate_speech'
            
            if is_toxic:
                toxic_count += 1
            else:
                normal_count += 1
            
            analyzed_comments.append({
                'comment_id': comment.get('comment_id', f'comment_{i}'),
                'author': comment.get('author', 'Unknown'),
                'text': comment.get('text', ''),
                'prediction': prediction['prediction'],
                'confidence': prediction['confidence'],
                'is_toxic':  is_toxic,
                'published_at': str(comment.get('published_at', ''))
            })
        # Filtrar solo tóxicos y ordenar por confidence (descendiente)
        toxic_comments = [c for c in analyzed_comments if c['is_toxic']]
        toxic_comments_sorted = sorted(
            toxic_comments,
            key=lambda x: x['confidence'],
            reverse=True
        )
        
        # Tomar top 10
        top_10_toxic = toxic_comments_sorted[:10]
        
        # Calcular porcentaje de toxicidad
        total_analyzed = len(analyzed_comments)
        toxicity_percentage = (toxic_count / total_analyzed * 100) if total_analyzed > 0 else 0.0
        
        logger.info(
            f"Análisis completado: {total_analyzed} comentarios, "
            f"{toxic_count} tóxicos ({toxicity_percentage:.2f}%)"
            )
        
        # Convertir a modelos Pydantic
        top_toxic_models = [CommentAnalysis(**comment) for comment in top_10_toxic]
        
        return YouTubeAnalysisOutput(
            video_id=video_id,
            video_title=video_title,            
            total_comments_analyzed=total_analyzed,            
            toxic_count=toxic_count,
            normal_count=normal_count,
            toxicity_percentage=round(toxicity_percentage, 2),
            top_toxic_comments=top_toxic_models,
            analysis_timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        # Re-raise HTTPExceptions (ya tienen el status code correcto)
        raise
    except Exception as e:
        logger.error(f"Error inesperado analizando video: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )
        
        


stats = {
    "lr_predictions": 0,
    "bert_predictions": 0,
    "comparisons": 0
}

@app.get("/stats", tags=["General"])
async def get_stats():
    """Retorna estadisticas de uso de la API."""
    return stats

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Permitir React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
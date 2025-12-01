"""
API REST para detección de hate speech en comentarios de YouTube.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.models.model_loader import HateSpeechDetector
import logging

#Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Inicializar FastAPI
app = FastAPI(
    title="YouTube Hate Speech Detector API",
    description="API para detectar mensajes de odio en comentarios de YouTube",
    version="1.0.0"
)

#Cargar modelo al inicio (singleton)
detector = None

@app.on_event("startup")
async def load_model():
    """Carga el modelo al iniciar la aplicación."""
    global detector
    try:
        detector = HateSpeechDetector()
        logger.info("✅ Modelo cargado exitosamente")
    except Exception as e:
        logger.error(f"❌ Error cargando modelo: {e}")
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
    model_loaded: bool
    model_type: Optional[str] = None


class ModelInfoResponse(BaseModel):
    """Modelo para información del modelo."""
    model_type: str
    threshold: float
    vectorizer_type: str
    vocab_size: int
    model_loaded: bool
    vectorizer_loaded: bool


# === ENDPOINTS ===    

@app.get("/", tags=["General"])
async def root():
    """Endpoint raíz de la API."""
    return {
        "message": "Youtube Hate Speech Detector API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict",
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
    model_loaded = detector is not None and detector.model is not None
    
    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        service="hate-speech-detector",
        model_loaded=model_loaded,
        model_type="Logistic Regression" if model_loaded else None
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
    Retorna información sobre el modelo cargado.
    
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
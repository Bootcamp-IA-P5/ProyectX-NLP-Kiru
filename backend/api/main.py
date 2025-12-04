"""
API REST para detección de hate speech en comentarios de YouTube.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.models.model_loader import HateSpeechDetector, DistilBERTDetector
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

@app.on_event("startup")
async def load_model():
    """Carga los modelos al iniciar la aplicación."""
    global detector, bert_detector
    try:
        detector = HateSpeechDetector()
        logger.info("✅ Modelo Logistic Regression cargado exitosamente")
        
        bert_detector = DistilBERTDetector()
        logger.info("✅ Modelo DistilBERT cargado exitosamente")
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
# 🛡️ YouTube Hate Speech Detector

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-green.svg)
![React](https://img.shields.io/badge/React-18.3.1-61DAFB.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Tests](https://img.shields.io/badge/tests-49%20passing-success.svg)
![Coverage](https://img.shields.io/badge/coverage-comprehensive-brightgreen.svg)

**Sistema de detección automática de mensajes de odio en comentarios de YouTube usando NLP y Deep Learning con DistilBERT**

[Características](#-características) • [Demo en Vivo](#-demo-en-vivo) • [Instalación](#-instalación) • [API](#-api-endpoints) • [Métricas](#-métricas-del-modelo)

</div>

---

## 📋 Descripción

YouTube enfrenta un aumento significativo en mensajes de odio entre los comentarios de sus vídeos. Este proyecto desarrolla una solución automatizada de detección usando **Procesamiento del Lenguaje Natural (NLP)** y **Deep Learning** con transformers (DistilBERT) para identificar y clasificar estos mensajes con alta precisión, permitiendo acciones de moderación escalables.

### 🎯 Problema
- Volumen masivo de comentarios imposible de moderar manualmente (miles por minuto)
- Costos prohibitivos de equipos de moderación humana 24/7
- Necesidad de escalabilidad y detección en tiempo real
- Falsos positivos que afectan la experiencia del usuario

### ✨ Solución
API REST robusta con frontend interactivo que analiza texto individual o videos completos de YouTube, detectando hate speech con **85.3% de precisión** usando DistilBERT fine-tuned y solo **5.3% de overfitting**.

---

## 🌐 Demo en Vivo

### 🚀 Backend API (Producción)
- **URL Base**: https://youtube-hate-speech-detector.onrender.com
- **Documentación Interactiva (Swagger)**: https://youtube-hate-speech-detector.onrender.com/docs
- **Health Check**: https://youtube-hate-speech-detector.onrender.com/health

### 💻 Frontend Local
El frontend React está disponible para ejecución local (instrucciones en [Instalación](#-instalación)).

**Características del Frontend:**
- 🎬 Análisis de videos completos de YouTube (hasta 200 comentarios)
- 📝 Predicción de texto individual en tiempo real
- 📊 Visualización de métricas del modelo (88% accuracy badge)
- 🎨 UI moderna con Tailwind CSS y animaciones
- 🔥 Botones de ejemplo para testing rápido
- 📈 Gráficas de toxicidad con código de colores

---

## 🚀 Características

### ✅ Completamente Implementado

#### 🤖 Machine Learning & NLP
- ✅ **Modelo DistilBERT fine-tuned** (85.3% accuracy, 83.9% F1-score)
- ✅ **Modelo Logistic Regression** optimizado como baseline (52.5% accuracy)
- ✅ **Preprocesamiento NLP** avanzado (NLTK + Spacy)
  - Tokenización, stemming (PorterStemmer), lemmatization
  - Stopwords removal, limpieza de URLs/menciones
  - Normalización de texto y vectorización TF-IDF
- ✅ **Data Augmentation** con NLPAUG (2x dataset → 1,994 samples)
- ✅ **Threshold optimization** para balance precision/recall

#### 🌐 Backend & API
- ✅ **FastAPI 1.0.0** con 9 endpoints RESTful
- ✅ **Análisis de videos de YouTube** (YouTube Data API v3)
  - Extracción de hasta 200 comentarios por video
  - Top 10 comentarios tóxicos rankeados por confianza
  - Metadata completa (autor, fecha, video title)
- ✅ **Predicción individual y por lotes** (hasta 100 textos)
- ✅ **Comparación de modelos** (LR vs DistilBERT)
- ✅ **Endpoints de estadísticas y health check**
- ✅ **CORS configurado** para desarrollo flexible

#### ⚛️ Frontend
- ✅ **React 18.3.1 + Vite 5.4.2** (desarrollo ultrarrápido)
- ✅ **Tailwind CSS 3.4.19** (diseño responsive y moderno)
- ✅ **Componentes interactivos**:
  - `VideoAnalyzer`: Input de URL, slider de comentarios, resultados con gráficas
  - `TextPredictor`: Análisis instantáneo con confidence scores
- ✅ **Métricas en vivo**: Display de accuracy, F1, parámetros, overfitting
- ✅ **Ejemplos pre-cargados**: Videos populares y textos de prueba
- ✅ **Animaciones fluidas**: Spinners, progress bars, fade-in effects

#### 🐳 DevOps & Testing
- ✅ **Docker** multi-stage (producción + desarrollo)
- ✅ **docker-compose** con hot-reload para dev
- ✅ **49 tests** unitarios (pytest) con cobertura comprehensive
  - 17 tests de preprocessing
  - 18 tests de modelos
  - 14 tests de endpoints API
- ✅ **Deployment en Render** (backend en producción)

#### 📊 Análisis & Experimentación
- ✅ **4 Jupyter Notebooks** completos:
  - EDA (Exploratory Data Analysis)
  - Preprocessing y modelos clásicos
  - DistilBERT con augmentation (NLPAUG)
  - Ensemble con XGBoost
- ✅ **Git LFS** para modelos grandes (255MB DistilBERT)

### 🗺️ Roadmap Futuro
- 📋 **MLflow** para tracking de experimentos
- 📋 **Base de datos SQLite** para persistencia de predicciones
- 📋 **Monitoreo en tiempo real** de streams de comentarios
- 📋 **Dashboard analítico** con Plotly/Streamlit
- 📋 **Frontend deployment** en Vercel/Netlify

---

## 🛠️ Tecnologías

### Core Stack
| Categoría | Tecnologías |
|-----------|-------------|
| **Backend** | FastAPI 1.0.0, Uvicorn, Pydantic |
| **ML/DL** | PyTorch 2.0+, Transformers 4.30+ (Hugging Face), Scikit-learn |
| **NLP** | NLTK, Spacy (en_core_web_sm), NLPAUG |
| **Frontend** | React 18.3.1, Vite 5.4.2, Tailwind CSS 3.4.19, Axios 1.7.2 |
| **YouTube** | google-api-python-client (YouTube Data API v3) |
| **Data** | Pandas, NumPy |
| **Optimización** | Optuna (hyperparameter tuning) |
| **DevOps** | Docker, docker-compose, Render |
| **Testing** | pytest, pytest-cov, httpx |

### Modelos
| Modelo | Accuracy | F1-Score | Overfitting | Estado |
|--------|----------|----------|-------------|--------|
| **DistilBERT** (fine-tuned) | **85.3%** | **83.9%** | **5.3%** | 🟢 Producción |
| Logistic Regression | 52.5% | 65.7% | 23.1% | 🟡 Baseline |

---

## 📦 Instalación

### Requisitos Previos
- Python 3.10+
- Node.js 18+ y npm (para frontend)
- Docker (opcional pero recomendado)
- Git y Git LFS (para clonar modelos grandes)
- YouTube Data API Key (para análisis de videos)

### Opción 1: Docker (Recomendado)

```bash
# Clonar repositorio
git clone https://github.com/Bootcamp-IA-P5/ProyectX-NLP-Kiru.git
cd ProyectX-NLP-Kiru

# Instalar Git LFS y descargar modelos
git lfs install
git lfs pull

# Configurar API key de YouTube
cp .env.example .env
# Editar .env y agregar: YOUTUBE_API_KEY=tu_api_key_aqui

# Ejecutar con Docker Compose
docker-compose up --build

# Solo backend producción (puerto 8000)
docker-compose up nlp-backend

# Backend desarrollo con hot-reload (puerto 8001)
docker-compose up nlp-dev
```

### Opción 2: Local (Desarrollo)

```bash
# Clonar repositorio
git clone https://github.com/Bootcamp-IA-P5/ProyectX-NLP-Kiru.git
cd ProyectX-NLP-Kiru

# Backend Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Configurar variables de entorno
export YOUTUBE_API_KEY=tu_api_key_aqui  # Linux/Mac
# set YOUTUBE_API_KEY=tu_api_key_aqui  # Windows

# Ejecutar backend
uvicorn backend.api.main:app --reload --port 8001

# Frontend Setup (nueva terminal)
cd frontend
npm install
npm run dev  # Corre en http://localhost:5173
```

### URLs de Acceso
- **Backend API**: `http://localhost:8001` (dev) o `http://localhost:8000` (prod)
- **Documentación Swagger**: `http://localhost:8001/docs`
- **Frontend**: `http://localhost:5173`

---

## 🔌 API Endpoints

### General

#### `GET /`
**Descripción**: Información de la API y modelos disponibles  
**Response**:
```json
{
  "message": "YouTube Hate Speech Detector API",
  "version": "1.0.0",
  "models_available": ["logistic_regression", "distilbert"],
  "endpoints": ["/predict", "/predict/transformer", "/analyze/video", ...],
  "docs": "/docs"
}
```

#### `GET /health`
**Descripción**: Health check del sistema y estado de modelos  
**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-12-11T10:30:00",
  "models_loaded": {
    "logistic_regression": true,
    "distilbert": true
  },
  "youtube_api": "configured"
}
```

#### `GET /stats`
**Descripción**: Estadísticas de uso de la API  
**Response**:
```json
{
  "total_predictions_lr": 1250,
  "total_predictions_bert": 3840,
  "total_comparisons": 120,
  "uptime_seconds": 86400
}
```

---

### Predicciones

#### `POST /predict`
**Descripción**: Predicción con Logistic Regression (baseline)  
**Request Body**:
```json
{
  "text": "I hate this stupid video and everyone who likes it"
}
```
**Response**:
```json
{
  "text": "I hate this stupid video and everyone who likes it",
  "prediction": "hate_speech",
  "confidence": 0.872,
  "model": "logistic_regression_threshold_0.3",
  "timestamp": "2024-12-11T10:35:00"
}
```

#### `POST /predict/transformer`
**Descripción**: Predicción con DistilBERT (recomendado) ⭐  
**Request Body**:
```json
{
  "text": "This is amazing! Great content, keep it up!"
}
```
**Response**:
```json
{
  "text": "This is amazing! Great content, keep it up!",
  "prediction": "normal",
  "confidence": 0.945,
  "probabilities": {
    "hate_speech": 0.055,
    "normal": 0.945
  },
  "model": "distilbert-base-uncased-finetuned",
  "timestamp": "2024-12-11T10:36:00"
}
```

#### `POST /predict/batch`
**Descripción**: Predicción por lotes (hasta 100 textos)  
**Request Body**:
```json
{
  "texts": [
    "Great video!",
    "This sucks, you are terrible",
    "Thanks for sharing this"
  ]
}
```
**Response**:
```json
{
  "predictions": [
    {
      "text": "Great video!",
      "prediction": "normal",
      "confidence": 0.921
    },
    {
      "text": "This sucks, you are terrible",
      "prediction": "hate_speech",
      "confidence": 0.784
    },
    {
      "text": "Thanks for sharing this",
      "prediction": "normal",
      "confidence": 0.956
    }
  ],
  "total_processed": 3,
  "model": "logistic_regression",
  "processing_time_seconds": 0.045
}
```

#### `POST /predict/compare`
**Descripción**: Compara predicciones de ambos modelos  
**Request Body**:
```json
{
  "text": "You are so dumb and worthless"
}
```
**Response**:
```json
{
  "text": "You are so dumb and worthless",
  "logistic_regression": {
    "prediction": "hate_speech",
    "confidence": 0.815
  },
  "distilbert": {
    "prediction": "hate_speech",
    "confidence": 0.923,
    "probabilities": {
      "hate_speech": 0.923,
      "normal": 0.077
    }
  },
  "agreement": true,
  "confidence_difference": 0.108
}
```

---

### YouTube Analysis

#### `POST /analyze/video` ⭐
**Descripción**: Analiza comentarios de un video de YouTube  
**Request Body**:
```json
{
  "url": "https://www.youtube.com/watch?v=9bZkp7q19f0",
  "max_comments": 200
}
```
**Response**:
```json
{
  "video_id": "9bZkp7q19f0",
  "video_title": "PSY - GANGNAM STYLE(강남스타일) M/V",
  "total_comments_analyzed": 200,
  "toxic_count": 52,
  "normal_count": 148,
  "toxicity_percentage": 26.0,
  "top_toxic_comments": [
    {
      "comment_text": "This is the worst thing I've ever seen...",
      "author": "user123",
      "confidence": 0.967,
      "published_at": "2024-11-15T08:30:00Z",
      "comment_id": "UgxKREjvS2SBSud4BpF4AaABAg"
    }
    // ... 9 more
  ],
  "analysis_timestamp": "2024-12-11T10:40:00",
  "model_used": "distilbert"
}
```

**Formatos de URL soportados:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID&t=120s`

---

### Model Info

#### `GET /model/info`
**Descripción**: Información detallada del modelo Logistic Regression  
**Response**:
```json
{
  "model_type": "LogisticRegression",
  "threshold": 0.3,
  "vectorizer": "TF-IDF",
  "vocab_size": 8547,
  "training_samples": 1395,
  "test_accuracy": 0.525,
  "f1_score": 0.657,
  "last_updated": "2024-11-20"
}
```

---

## 💻 Uso

### Ejemplos con curl

```bash
# Predicción simple con DistilBERT
curl -X POST "https://youtube-hate-speech-detector.onrender.com/predict/transformer" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your comment here"}'

# Análisis de video de YouTube
curl -X POST "https://youtube-hate-speech-detector.onrender.com/analyze/video" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=9bZkp7q19f0", "max_comments": 100}'

# Health check
curl "https://youtube-hate-speech-detector.onrender.com/health"
```

### Ejemplos con Python

```python
import requests

# Predicción con DistilBERT
response = requests.post(
    "https://youtube-hate-speech-detector.onrender.com/predict/transformer",
    json={"text": "This is an awesome video!"}
)
result = response.json()
print(f"Prediction: {result['prediction']}, Confidence: {result['confidence']}")

# Análisis de video
response = requests.post(
    "https://youtube-hate-speech-detector.onrender.com/analyze/video",
    json={
        "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
        "max_comments": 150
    }
)
analysis = response.json()
print(f"Toxicity: {analysis['toxicity_percentage']}%")
print(f"Toxic: {analysis['toxic_count']}, Normal: {analysis['normal_count']}")
```

### Frontend Local

```bash
cd frontend
npm run dev
# Abre http://localhost:5173 en tu navegador

# Características disponibles:
# - Tab "Video Analysis": Pegar URL de YouTube
# - Tab "Text Prediction": Escribir o usar ejemplos
# - Visualización de métricas del modelo
# - Botones de ejemplo para testing rápido
```

---

## 🏗️ Arquitectura del Proyecto

```
ProyectX-NLP-Kiru/
├── backend/
│   ├── api/
│   │   └── main.py                   # FastAPI app (579 líneas, 9 endpoints)
│   ├── models/
│   │   ├── model_loader.py           # HateSpeechDetector, DistilBERTDetector
│   │   ├── lr_threshold_optimized.pkl  # Modelo LR serializado
│   │   └── distilbert-hate-speech/   # Modelo DistilBERT fine-tuned (255MB)
│   │       ├── config.json
│   │       ├── model.safetensors     # Pesos del modelo
│   │       ├── tokenizer_config.json
│   │       └── vocab.txt
│   ├── preprocessing/
│   │   └── text_cleaner.py           # Pipeline NLP (tokenize, stem, clean)
│   ├── utils/
│   │   └── youtube_scraper.py        # YouTubeCommentFetcher class
│   └── __init__.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx                   # Main app con tabs y métricas
│   │   ├── components/
│   │   │   ├── VideoAnalyzer.jsx     # Componente de análisis de videos
│   │   │   └── TextPredictor.jsx     # Componente de predicción de texto
│   │   ├── services/
│   │   │   └── api.js                # Axios client (API integration)
│   │   ├── index.css                 # Tailwind + custom animations
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── data/
│   ├── raw/
│   │   └── youtoxic_english_1000.csv  # Dataset original (1000 samples)
│   └── processed/
│       ├── dataset_final_augmented.npz
│       └── dataset_ultra_augmented_600.npz  # 2x augmentation
├── notebooks/
│   ├── youtoxic_hatespeech_eda.ipynb              # EDA completo
│   ├── youtoxic_preprocessing_classic_models.ipynb
│   ├── youtoxic_DistilBERT_augmentation_NLPAUG.ipynb  # DistilBERT training
│   └── youtoxic_ensemble_xgboost_data_augmentation.ipynb
├── tests/
│   ├── test_preprocessing.py          # 17 tests
│   ├── test_model_loader.py           # 18 tests
│   ├── test_api_endpoints.py          # 14 tests
│   └── conftest.py
├── docker-compose.yml                 # Servicios: nlp-backend, nlp-dev
├── Dockerfile                         # Multi-stage: base + production
├── requirements.txt                   # 25+ dependencias Python
├── .dockerignore
├── .gitignore
├── .gitattributes                     # Git LFS para modelos grandes
└── README.md
```

---

## 📊 Métricas del Modelo

### 🏆 Modelo Principal: DistilBERT-base-uncased (Fine-tuned)

| Métrica | Train/Val | Test | Overfitting |
|---------|-----------|------|-------------|
| **Accuracy** | 90.6% | **85.3%** | **5.3%** ✅ |
| **F1-Score** | - | **83.9%** | - |
| **Precision** | - | **84.6%** | - |
| **Recall** | - | **83.3%** | - |

**Configuración del Modelo:**
- **Arquitectura**: DistilBERT-base-uncased (66M parámetros)
- **Dataset**: 1,994 samples (augmented 2x)
  - Train: 1,395 samples
  - Validation: 299 samples
  - Test: 300 samples
- **Entrenamiento**:
  - Epochs: 5
  - Batch size: 16
  - Learning rate: 2e-05
  - Weight decay: 0.01
  - Max sequence length: 128 tokens
- **Optimización**: AdamW optimizer
- **Framework**: PyTorch 2.0 + Transformers 4.30

### 📈 Modelo Baseline: Logistic Regression

| Métrica | Value |
|---------|-------|
| **Accuracy** | 52.5% |
| **F1-Score** | 65.7% |
| **Precision** | 49.2% |
| **Recall (Toxic)** | 98.9% ⚠️ |
| **Overfitting** | 23.1% ⚠️ |

**Configuración:**
- Vectorización: TF-IDF (8,547 features)
- Threshold optimizado: 0.3 (prioriza recall)
- Regularización: C=1.0

### 🆚 Comparación de Modelos

| Aspecto | DistilBERT | Logistic Regression |
|---------|------------|---------------------|
| **Accuracy** | ⭐⭐⭐⭐⭐ 85.3% | ⭐⭐ 52.5% |
| **F1-Score** | ⭐⭐⭐⭐⭐ 83.9% | ⭐⭐⭐ 65.7% |
| **Overfitting** | ⭐⭐⭐⭐⭐ 5.3% | ⭐⭐ 23.1% |
| **Velocidad** | ⭐⭐⭐ ~200ms | ⭐⭐⭐⭐⭐ ~20ms |
| **Memoria** | ⭐⭐ 255MB | ⭐⭐⭐⭐⭐ ~2MB |
| **Robustez** | ⭐⭐⭐⭐⭐ Alta | ⭐⭐⭐ Media |

**Recomendación**: DistilBERT para producción por superior accuracy, F1 y mínimo overfitting. LR útil para comparación y contextos con restricciones computacionales extremas.

---

## 🔬 Técnicas de NLP Aplicadas

### Preprocesamiento de Texto
1. **Lowercase conversion** - Normalización a minúsculas
2. **URL removal** - Eliminación de http/https links
3. **Punctuation cleaning** - Remoción de caracteres especiales
4. **Number removal** - Eliminación de dígitos
5. **Whitespace trimming** - Limpieza de espacios extras

### Técnicas Avanzadas
1. **Tokenización**: `nltk.word_tokenize`
2. **Stopwords removal**: English stopwords (NLTK corpus)
3. **Stemming**: PorterStemmer para normalización de palabras
4. **Vectorización**: TF-IDF (para LR), WordPiece Tokenizer (para DistilBERT)

### Data Augmentation (NLPAUG)
- **Técnicas**: Synonym replacement, back-translation, paraphrasing
- **Resultado**: Dataset expandido de 1,000 → 1,994 samples (2x)
- **Balance de clases**: Reducción de desbalance hate_speech/normal
- **Archivos generados**:
  - `dataset_final_augmented.npz`
  - `dataset_ultra_augmented_600.npz`

---

## 🧪 Testing

### Suite Completa: 49 Tests ✅

```bash
# Ejecutar todos los tests
pytest

# Con reporte de cobertura
pytest --cov=backend --cov-report=html

# Tests específicos
pytest tests/test_preprocessing.py     # 17 tests
pytest tests/test_model_loader.py      # 18 tests
pytest tests/test_api_endpoints.py     # 14 tests

# Ver reporte HTML
open htmlcov/index.html
```

### Breakdown por Módulo

#### `test_preprocessing.py` (17 tests)
- ✅ Limpieza de URLs y menciones
- ✅ Remoción de puntuación y números
- ✅ Tokenización y stopwords
- ✅ Stemming y normalización
- ✅ Pipeline completo de preprocessing

#### `test_model_loader.py` (18 tests)
- ✅ Carga de modelo Logistic Regression
- ✅ Carga de modelo DistilBERT
- ✅ Predicciones individuales y batch
- ✅ Formato de respuesta y tipos
- ✅ Comparación de modelos
- ✅ Manejo de errores

#### `test_api_endpoints.py` (14 tests)
- ✅ Endpoints `/`, `/health`, `/stats`, `/model/info`
- ✅ Endpoints de predicción: `/predict`, `/predict/transformer`, `/predict/batch`
- ✅ Validación de input (textos vacíos, demasiado largos)
- ✅ CORS headers
- ✅ Respuestas HTTP correctas

### Cobertura
- **Backend API**: Comprehensive (endpoints, validación, errores)
- **Preprocessing**: Comprehensive (todas las funciones)
- **Models**: Comprehensive (carga, predicción, comparación)

---

## 📝 Dataset

**Fuente**: YouTube Toxic Comments Dataset (Kaggle-style)

### Estadísticas
- **Muestras originales**: 1,000 comentarios
- **Tras augmentation**: 1,994 comentarios
- **Clases**: Binario (`hate_speech` | `normal`)
- **Idioma**: Inglés
- **Distribución**:
  - Train: 70% (1,395 samples)
  - Validation: 15% (299 samples)
  - Test: 15% (300 samples)

### Archivos de Datos
- `data/raw/youtoxic_english_1000.csv` - Dataset original
- `data/processed/dataset_final_augmented.npz` - Primera augmentation
- `data/processed/dataset_ultra_augmented_600.npz` - Augmentation 2x final

---

## 🐳 Docker

### Servicios

#### **nlp-backend** (Producción)
```bash
docker-compose up nlp-backend
```
- **Puerto**: 8000
- **Imagen**: Multi-stage optimizada
- **Health check**: Automático cada 30s
- **Restart policy**: unless-stopped
- **Uso**: Deployment en Render

#### **nlp-dev** (Desarrollo)
```bash
docker-compose up nlp-dev
```
- **Puerto**: 8001
- **Hot-reload**: Activado (uvicorn --reload)
- **Volúmenes**: Full project mount
- **DNS**: 8.8.8.8, 8.8.4.4
- **Uso**: Desarrollo local con auto-restart

### Dockerfile Multi-Stage

**Stage 1: Base**
- Python 3.10-slim
- Instalación de dependencias (requirements.txt)
- Descarga de modelo Spacy (en_core_web_sm)

**Stage 2: Production**
- COPY solo archivos necesarios
- Health check endpoint configurado
- CMD: `uvicorn backend.api.main:app --host 0.0.0.0 --port 8000`

---

## 🚀 Deployment

### Backend en Render

**URL**: https://youtube-hate-speech-detector.onrender.com

**Configuración**:
1. Repositorio: https://github.com/Bootcamp-IA-P5/ProyectX-NLP-Kiru
2. Branch: `dev` (o `main` según rama de producción)
3. Dockerfile: Detectado automáticamente
4. Variables de entorno:
   - `YOUTUBE_API_KEY=tu_api_key_aqui`
5. Plan: Free tier (suficiente para demo)

**Status**: ✅ Live y funcionando

**Endpoints de Verificación**:
- https://youtube-hate-speech-detector.onrender.com/
- https://youtube-hate-speech-detector.onrender.com/health
- https://youtube-hate-speech-detector.onrender.com/docs

### Frontend (Local)

El frontend está optimizado para ejecución local por ahora:

```bash
cd frontend
npm install
npm run dev  # http://localhost:5173
```

**Build para producción**:
```bash
npm run build  # Genera carpeta dist/
```

---

## 🎓 Notebooks de Experimentación

### 1. `youtoxic_hatespeech_eda.ipynb`
**Contenido**: Análisis Exploratorio de Datos (EDA)
- Distribución de clases
- Longitud de comentarios
- Palabras más frecuentes (wordclouds)
- Análisis de balance de dataset

### 2. `youtoxic_preprocessing_classic_models.ipynb`
**Contenido**: Preprocesamiento y modelos clásicos
- Pipeline de limpieza de texto
- Vectorización TF-IDF
- Modelos: Logistic Regression, SVM, Random Forest
- Comparación de accuracy/F1

### 3. `youtoxic_DistilBERT_augmentation_NLPAUG.ipynb`
**Contenido**: Entrenamiento de DistilBERT con augmentation ⭐
- Data augmentation con NLPAUG
- Fine-tuning de DistilBERT
- Evaluación completa (accuracy, F1, precision, recall)
- Análisis de overfitting
- Guardado del modelo final

### 4. `youtoxic_ensemble_xgboost_data_augmentation.ipynb`
**Contenido**: Experimentos con ensemble methods
- XGBoost classifier
- Data augmentation strategies
- Feature engineering
- Comparación con otros modelos

---

## 🤝 Contribución

Este es un proyecto académico de **Factoría F5 - Bootcamp IA (Promoción 5)**.

### Equipo
- **Desarrollador**: Kiru
- **Rol**: Data Scientist / ML Engineer / Full-Stack Developer
- **Institución**: Factoría F5
- **Programa**: Bootcamp de Inteligencia Artificial

### Guía para Contribuir (Futuros Forks)
1. Fork del repositorio
2. Crear branch: `git checkout -b feature/NuevaCaracteristica`
3. Commit cambios: `git commit -m "Add: Nueva característica"`
4. Push al branch: `git push origin feature/NuevaCaracteristica`
5. Abrir Pull Request

---

## 📄 Licencia

MIT License - ver archivo [LICENSE](LICENSE)

---

## 🔗 Enlaces Útiles

- **🌐 API en Producción**: https://youtube-hate-speech-detector.onrender.com
- **📚 Documentación API (Swagger)**: https://youtube-hate-speech-detector.onrender.com/docs
- **💻 Repositorio GitHub**: https://github.com/Bootcamp-IA-P5/ProyectX-NLP-Kiru
- **🤗 Hugging Face Transformers**: https://huggingface.co/transformers
- **📺 YouTube Data API**: https://developers.google.com/youtube/v3

---

## 📞 Contacto

**Proyecto desarrollado como parte del Bootcamp de IA - Factoría F5**

Para consultas sobre el proyecto: [GitHub Issues](https://github.com/Bootcamp-IA-P5/ProyectX-NLP-Kiru/issues)

---

## 🏆 Resultados y Logros

### ✅ Objetivos Cumplidos (Nivel Experto)
- ✅ **Implementación de Transformers** (DistilBERT fine-tuned)
- ✅ **API REST completa** con FastAPI (9 endpoints)
- ✅ **Frontend interactivo** con React + Tailwind
- ✅ **YouTube Integration** (análisis de videos completos)
- ✅ **Docker containerization** (multi-stage builds)
- ✅ **Testing comprehensive** (49 tests passing)
- ✅ **Deployment en producción** (Render)
- ✅ **Data augmentation** con NLPAUG
- ✅ **Overfitting < 10%** (5.3% achieved ✨)
- ✅ **Accuracy > 80%** (85.3% achieved ✨)

### 📈 Métricas Destacadas
- **85.3%** de accuracy en test set
- **83.9%** F1-score (balance precision/recall)
- **5.3%** de overfitting (excelente generalización)
- **200 comentarios/video** analizados en ~3 segundos
- **49 tests** unitarios (100% passing)

### 🎯 Impacto del Proyecto
Este proyecto demuestra una solución escalable y precisa para moderación automatizada de contenido en plataformas de video, con potencial de:
- Reducir costos de moderación manual en 70-80%
- Acelerar tiempo de respuesta de horas a segundos
- Mejorar experiencia de usuario con detección proactiva
- Escalar a millones de comentarios con infraestructura cloud

---

<div align="center">

⭐ **Si te gusta el proyecto, dale una estrella en GitHub!** ⭐

<sub>Construido con ❤️ usando FastAPI, DistilBERT, React y Docker</sub>

</div>

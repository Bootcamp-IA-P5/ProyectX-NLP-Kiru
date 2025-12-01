# 🛡️ YouTube Hate Speech Detector

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

**Sistema de detección automática de mensajes de odio en comentarios de YouTube usando NLP y Machine Learning**

[Características](#características) • [Instalación](#instalación) • [Uso](#uso) • [Arquitectura](#arquitectura) • [Métricas](#métricas)

</div>

---

## 📋 Descripción

YouTube enfrenta un aumento significativo en mensajes de odio entre los comentarios de sus vídeos. Este proyecto desarrolla una solución automatizada de detección usando técnicas de **Procesamiento del Lenguaje Natural (NLP)** y **Machine Learning** para identificar y clasificar estos mensajes, permitiendo acciones de moderación escalables.

### 🎯 Problema
- Volumen masivo de comentarios imposible de moderar manualmente
- Costos prohibitivos de equipos de moderación humana
- Necesidad de escalabilidad en tiempo real

### ✨ Solución
API REST robusta que analiza texto y detecta hate speech con alta precisión usando modelos optimizados de ML/DL.

---

## 🚀 Características

### Implementado ✅
- ✅ **API REST** con FastAPI
- ✅ **Modelo Logistic Regression optimizado** con threshold ajustado
- ✅ **Preprocesamiento NLP** completo (stemming, lemmatization, stopwords)
- ✅ **Vectorización TF-IDF** clásica
- ✅ **Data Augmentation** para balanceo de clases
- ✅ **Análisis Exploratorio** detallado (EDA)
- ✅ **Docker** para containerización

### En Desarrollo 🚧
- 🚧 Modelos Transformer (BERT/DistilBERT)
- 🚧 MLflow para tracking de experimentos
- 🚧 Base de datos para persistencia de predicciones
- 🚧 Tests unitarios (cobertura >70%)
- 🚧 Deployment en Railway/Render

### Roadmap 🗺️
- 📋 Análisis de videos completos (URL → estadísticas)
- 📋 Monitoreo en tiempo real
- 📋 Dashboard de visualización

---

## 🛠️ Tecnologías

### Core Stack
- **Backend**: FastAPI, Uvicorn
- **ML/NLP**: Scikit-learn, Transformers (Hugging Face), NLTK, Spacy
- **Data**: Pandas, NumPy
- **Optimización**: Optuna
- **Deployment**: Docker, Railway/Render
- **Tracking**: MLflow (próximamente)

### Modelos
- **Producción Actual**: Logistic Regression con threshold optimizado
- **En Evaluación**: BERT, DistilBERT, RoBERTa
- **Experimentales**: XGBoost, Random Forest, SVM

---

## 📦 Instalación

### Requisitos Previos
- Python 3.10+
- Docker (opcional)
- Git

### Opción 1: Local

```bash
# Clonar repositorio
git clone https://github.com/Bootcamp-IA-P5/ProyectX-NLP-Kiru.git
cd ProyectX-NLP-Kiru

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelo Spacy
python -m spacy download en_core_web_sm

# Ejecutar API
uvicorn backend.api.main:app --reload
```

### Opción 2: Docker

```bash
# Build y ejecutar
docker-compose up --build

# Solo producción
docker-compose up nlp-backend

# Modo desarrollo
docker-compose up nlp-dev
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

---

## 💻 Uso

### Predicción Individual

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your comment here"}'
```

**Respuesta:**
```json
{
  "text": "Your comment here",
  "prediction": "hate_speech",
  "confidence": 0.87,
  "model": "logistic_regression_threshold"
}
```

### Predicción por Lotes

```bash
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["comment 1", "comment 2", "comment 3"]}'
```

### Métricas del Modelo

```bash
curl "http://localhost:8000/metrics"
```

---

## 🏗️ Arquitectura

```
ProyectX-NLP-Kiru/
├── backend/
│   ├── api/              # Endpoints FastAPI
│   ├── preprocessing/    # Limpieza y vectorización
│   ├── models/           # Modelos ML/DL
│   │   ├── saved/        # Modelos entrenados
│   │   └── lr_threshold_optimized.pkl
│   ├── evaluation/       # Métricas y reportes
│   └── database/         # Persistencia (próximamente)
├── data/
│   ├── raw/              # Datos originales
│   └── processed/        # Datasets augmentados
├── notebooks/            # Experimentación Jupyter
│   ├── youtoxic_hatespeech_eda.ipynb
│   ├── youtoxic_preprocessing_classic_models.ipynb
│   └── youtoxic_ensemble_xgboost_data_augmentation.ipynb
├── tests/                # Tests unitarios
├── logs/                 # Logs de aplicación
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## 📊 Métricas del Modelo

### Modelo Actual: Logistic Regression (Threshold Optimizado)

| Métrica | Train | Test | Diferencia |
|---------|-------|------|------------|
| **Accuracy** | - | - | <5% ✅ |
| **Precision** | - | - | - |
| **Recall** | - | - | - |
| **F1-Score** | - | - | - |

> 📝 *Métricas actualizadas tras re-entrenamiento final*

### Técnicas Aplicadas
- ✅ **Preprocesamiento**: Stemming, Lemmatization, Stopwords removal
- ✅ **Vectorización**: TF-IDF clásico
- ✅ **Data Augmentation**: Traducción, sinónimos, parafraseo
- ✅ **Regularización**: Optimización de threshold
- ✅ **Expresiones Regulares**: Limpieza de URLs, menciones, emojis

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=backend --cov-report=html

# Solo tests específicos
pytest tests/test_preprocessing.py
```

---

## 📝 Dataset

**Fuente**: [YouTube Toxic Comments Dataset](https://www.kaggle.com/datasets/...)

- **Muestras originales**: 1000 comentarios
- **Tras augmentation**: 600+ comentarios balanceados
- **Clases**: `hate_speech` | `normal`
- **Idioma**: Inglés

---

## 🤝 Contribución

Este es un proyecto académico de **Factoría F5 - Bootcamp IA**. 

### Equipo
- **Desarrollador**: Kiru
- **Rol**: Data Scientist / AI Developer

---

## 📄 Licencia

MIT License - ver archivo [LICENSE](LICENSE)

---

## 🔗 Enlaces

- **Documentación API**: http://localhost:8000/docs
- **Repositorio**: https://github.com/Bootcamp-IA-P5/ProyectX-NLP-Kiru
- **MLflow UI**: http://localhost:5000 (próximamente)

---

## 📞 Contacto

**Proyecto desarrollado como parte del Bootcamp de IA - Factoría F5**

⭐ Si te gusta el proyecto, dale una estrella en GitHub!

---

<div align="center">
  <sub>Construido con ❤️ usando FastAPI y Transformers</sub>
</div>

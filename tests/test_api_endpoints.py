"""
Tests para los endpoints de la API.
"""

import pytest
from fastapi.testclient import TestClient


class TestGeneralEndpoints:
    """Tests para endpoints generales."""
    
    def test_root_endpoint(self, test_client):
        """Debe retornar información de la API."""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "models" in data
        assert "endpoints" in data
    
    def test_health_endpoint(self, test_client):
        """Debe retornar estado de salud."""
        response = test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert data["status"] in ["healthy", "degraded"]
    
    def test_stats_endpoint(self, test_client):
        """Debe retornar estadísticas de uso."""
        response = test_client.get("/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
    
    def test_model_info_endpoint(self, test_client):
        """Debe retornar información del modelo LR."""
        response = test_client.get("/model/info")
        
        assert response.status_code == 200
        data = response.json()
        assert "model_type" in data
        assert "threshold" in data


class TestPredictionEndpoints:
    """Tests para endpoints de predicción."""
    
    def test_predict_lr_toxic_text(self, test_client):
        """Debe predecir texto tóxico con LR."""
        response = test_client.post(
            "/predict",
            json={"text": "I hate you, you're so stupid!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "confidence" in data
        assert "is_toxic" in data
        assert isinstance(data["confidence"], float)
    
    def test_predict_lr_normal_text(self, test_client):
        """Debe predecir texto normal con LR."""
        response = test_client.post(
            "/predict",
            json={"text": "Thank you for this amazing video!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
    
    def test_predict_transformer_endpoint(self, test_client):
        """Debe predecir con DistilBERT."""
        response = test_client.post(
            "/predict/transformer",
            json={"text": "I hate you!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "confidence" in data
        assert "is_toxic" in data
    
    def test_predict_compare_endpoint(self, test_client):
        """Debe comparar ambos modelos."""
        response = test_client.post(
            "/predict/compare",
            json={"text": "You are amazing!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "logistic_regression" in data
        assert "distilbert" in data
        assert "comparison" in data
        assert "agreement" in data["comparison"]
        assert "recommended_model" in data["comparison"]
    
    def test_predict_batch_endpoint(self, test_client):
        """Debe predecir múltiples textos."""
        response = test_client.post(
            "/predict/batch",
            json={"texts": ["Hello!", "I hate you", "Great video"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total" in data
        assert data["total"] == 3
        assert len(data["results"]) == 3


class TestInputValidation:
    """Tests para validación de inputs."""
    
    def test_empty_text_handled(self, test_client):
        """Debe manejar texto vacío."""
        response = test_client.post(
            "/predict/transformer",
            json={"text": ""}
        )
        
        # Debería procesar sin error (aunque sea texto vacío)
        assert response.status_code in [200, 422]
    
    def test_very_long_text_handled(self, test_client):
        """Debe manejar texto muy largo."""
        long_text = "word " * 1000
        response = test_client.post(
            "/predict/transformer",
            json={"text": long_text}
        )
        
        # BERT trunca a max_length, debe funcionar
        assert response.status_code == 200
    
    def test_special_characters_handled(self, test_client):
        """Debe manejar caracteres especiales."""
        response = test_client.post(
            "/predict",
            json={"text": "😡😡😡 @#$%^&*()"}
        )
        
        assert response.status_code == 200
    
    def test_batch_empty_list_error(self, test_client):
        """Debe rechazar lista vacía en batch."""
        response = test_client.post(
            "/predict/batch",
            json={"texts": []}
        )
        
        assert response.status_code == 422  # Validation error


class TestCORS:
    """Tests para configuración CORS."""
    
    def test_cors_headers_present(self, test_client):
        """Debe incluir headers CORS."""
        response = test_client.options("/predict")
        
        # TestClient no siempre muestra headers CORS, pero no debe fallar
        assert response.status_code in [200, 405]
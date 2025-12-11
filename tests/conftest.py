"""
Fixtures compartidas para los tests.
"""

import pytest
from fastapi.testclient import TestClient
from backend.api.main import app
from backend.models.model_loader import HateSpeechDetector, DistilBERTDetector

@pytest.fixture(scope="session")
def sample_texts():
    """Textos de ejemplo para tests."""
    return {
        "toxic": [
            "I hate you, you're so stupid!",
            "Go kill yourself",
            "You're a worthless piece of trash",
            "Die in a fire"
        ],
        "normal": [
            "I love this video!",
            "Great content, thanks for sharing",
            "This is really helpful",
            "You are amazing"
        ],
        "edge_cases": [
            "",  # Texto vacío
            "   ",  # Solo espacios
            "a",  # Un solo carácter
            "http://spam.com",  # Solo URL
            "😡😡😡",  # Solo emojis
        ]
    }

@pytest.fixture(scope="session")
def lr_detector():
    """Instancia del detector Logistic Regression."""
    try: 
        detector = HateSpeechDetector()
        return detector
    except Exception as e:
        pytest.skip(f"No se pudo cargar modelo LR: {e}")

@pytest.fixture(scope="session")
def bert_detector():
    """Instancia del detector DistilBERT."""
    try:
        detector = DistilBERTDetector()
        return detector
    except Exception as e:
        pytest.skip(f"No se pudo cargar modelo BERT: {e}")


@pytest.fixture(scope="module")
def test_client():
    """Cliente de pruebas para la API."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_toxic_text():
    """Texto tóxico individual."""
    return "I hate you, you're so stupid!"


@pytest.fixture
def sample_normal_text():
    """Texto normal individual."""
    return "Thank you for this amazing video!"

    
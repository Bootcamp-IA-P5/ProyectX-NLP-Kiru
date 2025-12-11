"""
Tests para el módulo de preprocesamiento de texto.
"""

import pytest
from backend.preprocessing.text_cleaner import clean_text, preprocess_text, full_preprocess

class TestCleanText:
    """Tests para la función clean_text."""
    def test_removes_urls(self):
        """Debe eliminar URLs del texto."""
        text = "Check this out http://spam.com and https://evil.org"
        result = clean_text(text)
        assert "http" not in result
        assert "spam.com" not in result
        assert "evil.org" not in result 
        
    def test_removes_punctuation(self):
        """Debe eliminar signos de puntuación."""
        text = "Hello! How are you? I'm fine, thanks."
        result = clean_text(text)
        assert "!" not in result
        assert "?" not in result
        assert "," not in result
        assert "'" not in result
    
    def test_converts_to_lowercase(self):
        """Debe convertir texto a minúsculas."""
        text = "HELLO WoRlD"
        result = clean_text(text)
        assert result == "hello world"
    
    def test_removes_numbers(self):
        """Debe eliminar números del texto."""
        text = "I have 3 cats and 2 dogs in 2024"
        result = clean_text(text)
        assert "3" not in result
        assert "2" not in result
        assert "2024" not in result
        
    def test_strips_whitespace(self):
        """Debe eliminar espacios al inicio y final."""
        text = "   hello world   "
        result = clean_text(text)
        assert result == "hello world"
    
    def test_empty_string(self):
        """Debe manejar strings vacíos."""
        result = clean_text("")
        assert result == ""
    
    def test_only_punctuation(self):
        """Debe manejar texto que solo tiene puntuación."""
        text = "!@#$%^&*()"
        result = clean_text(text)
        assert result == ""

class TestPreprocessText:
    """Tests para la función preprocess_text."""
    
    def test_removes_stopwords(self):
        """Debe eliminar stopwords en inglés."""
        text = "the cat is on the table"
        result = preprocess_text(text)
        assert "the" not in result
        assert "is" not in result
        assert "on" not in result
    
    def test_applies_stemming(self):
        """Debe aplicar stemming a las palabras."""
        text = "running runs runner"
        result = preprocess_text(text)
        # Todas deberían reducirse a "run"
        assert len(set(result)) == 1
        assert all("run" in token for token in result)
    
    def test_tokenizes_correctly(self):
        """Debe tokenizar correctamente."""
        text = "hello world"
        result = preprocess_text(text)
        assert isinstance(result, list)
        assert len(result) == 2
        
     
class TestPreprocessText:
    """Tests para la función preprocess_text."""
    
    def test_removes_stopwords(self):
        """Debe eliminar stopwords en inglés."""
        text = "the cat is on the table"
        result = preprocess_text(text)
        assert "the" not in result
        assert "is" not in result
        assert "on" not in result
    
    def test_applies_stemming(self):
        """Debe aplicar stemming a las palabras."""
        text = "running runs"
        result = preprocess_text(text)
        # Ambas deberían reducirse a "run"
        assert len(set(result)) == 1
        assert all("run" in token for token in result)
    
    def test_tokenizes_correctly(self):
        """Debe tokenizar correctamente."""
        text = "hello world"
        result = preprocess_text(text)
        assert isinstance(result, list)
        assert len(result) == 2   
    
    def test_empty_text_returns_empty_list(self):
        """Debe retornar lista vacía para texto vacío."""
        result = preprocess_text("")
        assert result == []
    
    def test_whitespace_only_returns_empty_list(self):
        """Debe retornar lista vacía para solo espacios."""
        result = preprocess_text("   ")
        assert result == []


class TestFullPreprocess:
    """Tests para el pipeline completo."""
    
    def test_full_pipeline(self):
        """Debe aplicar todo el pipeline correctamente."""
        text = "I HATE you! You're so STUPID! http://spam.com"
        result = full_preprocess(text)
        
        # Debe estar en minúsculas
        assert result == result.lower()
        
        # No debe contener puntuación
        assert "!" not in result
        assert "'" not in result
        
        # No debe contener URLs
        assert "http" not in result
    
    def test_returns_string(self):
        """Debe retornar un string, no una lista."""
        text = "hello world"
        result = full_preprocess(text)
        assert isinstance(result, str)
    
    def test_empty_input(self):
        """Debe manejar input vacío."""
        result = full_preprocess("")
        assert result == ""
    
    def test_toxic_comment_preprocessing(self):
        """Debe preprocesar comentario tóxico correctamente."""
        text = "Go DIE you STUPID idiot!!!"
        result = full_preprocess(text)
        
        # Debe contener stems de las palabras clave
        assert len(result) > 0
        assert result == result.lower()
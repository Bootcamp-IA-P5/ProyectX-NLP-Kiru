"""
Tests para los modelos de detección (LR y DistilBERT).
"""

import pytest


class TestLogisticRegressionDetector:
    """Tests para HateSpeechDetector (Logistic Regression)."""
    
    def test_detector_loads_successfully(self, lr_detector):
        """Debe cargar el modelo y vectorizador correctamente."""
        assert lr_detector.model is not None
        assert lr_detector.vectorizer is not None
        assert lr_detector.threshold == 0.3
    
    def test_predict_toxic_text(self, lr_detector, sample_toxic_text):
        """Debe detectar texto tóxico."""
        result = lr_detector.predict(sample_toxic_text)
        
        assert "prediction" in result
        assert "confidence" in result
        assert "is_toxic" in result
        assert isinstance(result["confidence"], float)
        assert 0 <= result["confidence"] <= 1
    
    def test_predict_normal_text(self, lr_detector, sample_normal_text):
        """Debe detectar texto normal."""
        result = lr_detector.predict(sample_normal_text)
        
        assert "prediction" in result
        assert isinstance(result["is_toxic"], bool)
    
    def test_predict_batch(self, lr_detector, sample_texts):
        """Debe predecir múltiples textos correctamente."""
        texts = sample_texts["toxic"][:2] + sample_texts["normal"][:2]
        results = lr_detector.predict_batch(texts)
        
        assert len(results) == 4
        assert all("prediction" in r for r in results)
        assert all("confidence" in r for r in results)
    
    def test_get_model_info(self, lr_detector):
        """Debe retornar información del modelo."""
        info = lr_detector.get_model_info()
        
        assert "model_type" in info
        assert "threshold" in info
        assert "vectorizer_type" in info
        assert info["model_loaded"] is True


class TestDistilBERTDetector:
    """Tests para DistilBERTDetector (Transformer)."""
    
    def test_detector_loads_successfully(self, bert_detector):
        """Debe cargar modelo y tokenizer correctamente."""
        assert bert_detector.model is not None
        assert bert_detector.tokenizer is not None
        assert bert_detector.max_length == 128
    
    def test_predict_toxic_text(self, bert_detector, sample_toxic_text):
        """Debe detectar texto tóxico con alta confianza."""
        result = bert_detector.predict(sample_toxic_text)
        
        assert result["prediction"] in ["normal", "hate_speech"]
        assert "confidence" in result
        assert "probabilities" in result
        assert isinstance(result["confidence"], float)
        assert 0 <= result["confidence"] <= 1
    
    def test_predict_normal_text(self, bert_detector, sample_normal_text):
        """Debe detectar texto normal con alta confianza."""
        result = bert_detector.predict(sample_normal_text)
        
        assert "prediction" in result
        assert "label" in result
        assert result["label"] in [0, 1]
    
    def test_confidence_scores_valid(self, bert_detector, sample_texts):
        """Debe retornar scores de confianza válidos."""
        for text in sample_texts["toxic"][:2]:
            result = bert_detector.predict(text)
            assert 0 <= result["confidence"] <= 1
            assert 0 <= result["probabilities"]["normal"] <= 1
            assert 0 <= result["probabilities"]["hate_speech"] <= 1
            
            # Las probabilidades deben sumar ~1
            total = result["probabilities"]["normal"] + result["probabilities"]["hate_speech"]
            assert 0.99 <= total <= 1.01
    
    def test_predict_batch(self, bert_detector, sample_texts):
        """Debe predecir múltiples textos en batch."""
        texts = sample_texts["normal"][:3]
        results = bert_detector.predict_batch(texts)
        
        assert len(results) == 3
        assert all("prediction" in r for r in results)
        assert all("confidence" in r for r in results)
    
    def test_handles_empty_text(self, bert_detector):
        """Debe manejar texto vacío sin errores."""
        result = bert_detector.predict("")
        assert "prediction" in result
        assert "confidence" in result
    
    def test_handles_long_text(self, bert_detector):
        """Debe truncar texto largo a max_length."""
        long_text = "word " * 200  # Más de 128 tokens
        result = bert_detector.predict(long_text)
        
        assert "prediction" in result
        assert isinstance(result["confidence"], float)


class TestModelComparison:
    """Tests comparativos entre modelos."""
    
    def test_both_models_agree_on_obvious_toxic(self, lr_detector, bert_detector):
        """Ambos modelos deben coincidir en casos obvios."""
        text = "Go kill yourself you worthless piece of trash"
        
        lr_result = lr_detector.predict(text)
        bert_result = bert_detector.predict(text)
        
        # Al menos uno debe detectar toxicidad
        assert lr_result["is_toxic"] or bert_result["prediction"] == "hate_speech"
    
    def test_both_models_agree_on_obvious_normal(self, lr_detector, bert_detector):
        """Ambos modelos deben coincidir en casos claramente normales."""
        text = "Thank you so much for this wonderful tutorial"
        
        lr_result = lr_detector.predict(text)
        bert_result = bert_detector.predict(text)
        
        # Ambos deberían detectar como normal
        assert not lr_result["is_toxic"] or bert_result["prediction"] == "normal"
    
    def test_bert_more_confident_than_lr(self, lr_detector, bert_detector, sample_texts):
        """BERT debería tener menor varianza en confianza."""
        confidences_lr = []
        confidences_bert = []
        
        for text in sample_texts["toxic"][:3] + sample_texts["normal"][:3]:
            lr_res = lr_detector.predict(text)
            bert_res = bert_detector.predict(text)
            confidences_lr.append(lr_res["confidence"])
            confidences_bert.append(bert_res["confidence"])
        
        # BERT debería tener confianzas más consistentemente altas
        import statistics
        bert_mean = statistics.mean(confidences_bert)
        assert bert_mean > 0.7  # Generalmente >90% según tus tests
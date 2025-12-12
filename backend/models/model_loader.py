"""
Módulo para cargar y usar el modelo de detección de hate speech.
Utiliza Logistic Regression con threshold optimizado (0.3) y vectorizador TF-IDF.
"""

import pickle
import os
from pathlib import Path
import numpy as np
from backend.preprocessing.text_cleaner import full_preprocess
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


# Clase stub para deserializar modelos antiguos
class LRThresholdModel:
    """Stub para cargar modelos pickle antiguos que usan esta clase."""
    def __init__(self, model=None, threshold=0.3):
        self.model = model
        self.threshold = threshold

class HateSpeechDetector:
    """
    Detector de mensajes de odio usando Logistic Regression optimizado.
    """
    
    def __init__(self, model_path=None, vectorizer_path=None, threshold=0.3):
        """
        Inicializa el detector de hate speech.
        
        Args:
            model_path (str): Ruta al archivo .pkl del modelo LR
            vectorizer_path (str): Ruta al archivo .pkl del vectorizador TF-IDF
            threshold (float): Umbral de decisión optimizado (default 0.3)
        """
        self.threshold = threshold
        self.model = None
        self.vectorizer = None
        
        # Rutas por defecto
        if model_path is None:
            base_path = Path(__file__).parent
            model_path = base_path / "lr_threshold_optimized.pkl"
            
        if vectorizer_path is None:
            base_path = Path(__file__).parent
            vectorizer_path = base_path / "tfidf_vectorizer.pkl"
        
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        
        # Cargar modelos automaticamente
        self.load_models()
        
    def load_models(self):
        """
        Carga el modelo LR y el vectorizador TF-IDF desde path
        """
        try:
            # Cargar modelo con unpickler personalizado para manejar clases faltantes
            import sys
            import types
            
            # Crear módulo temporal con la clase stub
            temp_module = types.ModuleType('temp_module')
            temp_module.LRThresholdModel = LRThresholdModel
            sys.modules['__main__'].LRThresholdModel = LRThresholdModel
            sys.modules['__mp_main__'] = temp_module
            
            class CustomUnpickler(pickle.Unpickler):
                def find_class(self, module, name):
                    if name == 'LTRhresholdModel':
                        return LRThresholdModel
                    return super().find_class(module, name)
            
            # Cargar modelo con unpickler personalizado
            with open(self.model_path, 'rb') as f:
               loaded = CustomUnpickler(f).load()
               
               # Manejar diferentes formatos de guardado
               if isinstance(loaded, LRThresholdModel):
                   # Modelo envuelto en clase custom
                   self.model = loaded.model
                   if hasattr(loaded, 'threshold'):
                       self.threshold = loaded.threshold
               elif isinstance(loaded, dict):
                   # Modelo guardado como diccionario
                   self.model = loaded.get('model', loaded)
               else:
                   # Modelo directo (LogisticRegression)
                   self.model = loaded
                   
            print(f"✅ Modelo cargado: {self.model_path}")
            print(f"   Tipo: {type(self.model)}")
            
            # Cargar vectorizador
            with open(self.vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            print(f"✅ Vectorizador cargado: {self.vectorizer_path}")

        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"No se encontraron los archivos del modelo. "
                f"Verifica que existan:\n- {self.model_path}\n- {self.vectorizer_path}"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Error cargando modelos: {e}") from e
    
    def predict(self, text):
        """
        Predice si un texto es hate speech o no.
        
        Args:
            text (str): Texto del comentario a analizar
            
        Returns:
            dict: {
                'text': texto original,
                'prediction': 'hate_speech' | 'normal',
                'confidence': float (0-1),
                'is_toxic': bool
            }
        """
        if self.model is None or self.vectorizer is None:
            raise RuntimeError("Modelos no cargados. Llama a load_models() primero.")
        
        # Preprocesar texto
        cleaned_text = full_preprocess(text)
        
        # Vectorizar
        X = self.vectorizer.transform([cleaned_text])
        
        # Predecir probabilidad
        proba = self.model.predict_proba(X)[0, 1]  # Probabilidad de clase 'toxic'
        
        # Determinar etiqueta basada en el umbral
        is_toxic = proba >= self.threshold
        
        # Formatear resultado
        return {
            'text': text,
            'prediction': 'hate_speech' if is_toxic else 'normal',
            'confidence': float(proba),
            'is_toxic': bool(is_toxic),
            'threshold_used': self.threshold,
            'model': f'logistic_regression_threshold_{self.threshold}'
        }
    
    def predict_batch(self, texts):
        """
        Predice múltiples textos de una vez (más eficiente).
        
        Args:
            texts (list): Lista de strings a analizar
            
        Returns:
            list: Lista de diccionarios con resultados
        """
        if self.model is None or self.vectorizer is None:
            raise RuntimeError ("Modelos no cargados.")
        
        # 1. Preprocesar todos los textos
        processed_texts = [full_preprocess(text) for text in texts]        
        
        # 2. Vectorizar todos de una vez
        X = self.vectorizer.transform(processed_texts)
        
        # 3. Predecir todas las probabilidades
        probas = self.model.predict_proba(X)[:,1]
        
        # 4. Aplicar threshold
        predictions = probas >= self.threshold
        
        # 5. Formatear resultados
        results = []
        for text, proba, is_toxic in zip(texts, probas, predictions):
            results.append({
                'text': text,
                'prediction': 'hate_speech' if is_toxic else 'normal',
                'confidence': float(proba),
                'is_toxic': bool(is_toxic),
                'threshold_used': self.threshold
            })
            
        return results
    
    def get_model_info(self):
        """
        Retorna información sobre el modelo cargado.
        
        Returns:
            dict: Información del modelo
        """
        return {
            'model_type': 'Logistic Regression',
            'threshold': self.threshold,
            'vectorizer_type': 'TF-IDF',
            'vocab_size': len(self.vectorizer.vocabulary_) if self.vectorizer else 0,
            'model_loaded': self.model is not None,
            'vectorizer_loaded': self.vectorizer is not None        
        }        

class DistilBERTDetector:
    """
    Detector de hate speech usando DistilBERT fine-tuned.
    """

    def __init__(self, model_path=None):
        """Inicializa el detector DistilBERT"""
        #Ruta por defecto
        if model_path is None:
            base_path = Path(__file__).parent
            model_path = base_path / "distilbert-hate-speech"
        
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.max_length = 128
        self.labels = {0: "normal", 1: "hate_speech"}
        
        # Cargar modelo automáticamente
        self.load_model()
        
    def load_model(self):
        """Carga el modelo DistilBERT y tokenizer desde disco."""
        try:
            print(f"🤖 Cargando modelo DistilBERT desde {self.model_path}...")
            
            # Cargar tokenizer y modelo
            self.tokenizer = AutoTokenizer.from_pretrained(str(self.model_path))
            self.model = AutoModelForSequenceClassification.from_pretrained(str(self.model_path))
            
            # Modo evaluación (desactiva dropout)
            self.model.eval()
            
            print("✅ Modelo DistilBERT cargado correctamente!")
            print(f"   Parámetros: {self.model.num_parameters():,}")
            
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f"No se encontró el modelo DistilBERT en: {self.model_path}\n"
                f"Asegúrate de que la carpeta contenga los archivos del modelo."
            ) from e
        except Exception as e:
            raise RuntimeError(f"Error cargando modelo DistilBERT: {e}") from e

    def predict (self, text):
        """
        Predice si un texto contiene hate speech.
        
        Args:
            text (str): Texto a analizar
            
        Returns:
            dict: {
                'text': texto original,
                'prediction': 'hate_speech' | 'normal',
                'confidence': float (0-1),
                'label': int (0=normal, 1=hate_speech),
                'probabilities': {'normal': float, 'hate_speech': float}
            }
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Modelo no cargado. Llama a load_model() primero")
        
        # 1. Tokenizer (texto >> tensores numericos)
        inputs = self.tokenizer(
            text,
            max_length=self.max_length,
            truncation=True,
            padding=True,
            return_tensors="pt" # PyTorch tensors
        )
        
        # 2. Predecir (sin calcular gradientes = mas rapido)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)
            
            # Extraer predicción
            predicted_class = torch.argmax(probs, dim=-1).item() # 0 o 1
            confidence = probs[0][predicted_class].item()        # Confianza de la prediccion
            
            # Probabilidades individuales
            prob_normal = probs[0][0].item()
            prob_hate = probs[0][1].item()
            
        # 3. Formatear resultado
        return {
            'text': text,
            'prediction': self.labels[predicted_class],
            'confidence': float(confidence),
            'label': int(predicted_class),
            'probabilities': {
                'normal': float(prob_normal),
                'hate_speech': float(prob_hate)
            }
        }
    def predict_batch(self, texts):
        """
        Predice múltiples textos de una vez (más eficiente que llamar predict() varias veces).
        
        Args:
            texts (list): Lista de strings a analizar
            
        Returns:
            list: Lista de diccionarios con resultados
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Modelo no cargado.")
        
        # 1. Tokenizar todos los textos juntos (batch processing)
        inputs = self.tokenizer(
            texts,
            max_length=self.max_length,
            truncation=True,
            padding=True,
            return_tensors="pt"
        )
        
        # 2. Predecir todo el batch de una vez
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)
            
            predicted_classes = torch.argmax(probs, dim=1)
            confidences = probs[range(len(texts)), predicted_classes]
            
        # 3. Formatear resultados para cada texto
        results = []
        for i, text in enumerate(texts):
            predicted_class = predicted_classes[i].item()
            confidence = confidences[i].item()
            prob_normal = probs[i][0].item()
            prob_hate = probs[i][1].item()
            
            results.append({
                'text': text,
                'prediction': self.labels[predicted_class],
                'confidence': float(confidence),
                'label': int(predicted_class),
                'probabilities': {
                    'normal': float(prob_normal),
                    'hate_speech': float(prob_hate)
                }
            })
        
        return results
    
    def get_model_info(self):
        """
        Retorna información sobre el modelo DistilBERT.
        
        Returns:
            dict: Información del modelo
        """
        return {
            'model_type': 'DistilBERT-base-uncased',
            'task': 'hate_speech_detection',
            'num_parameters': self.model.num_parameters() if self.model else 0,
            'max_length': self.max_length,
            'labels': self.labels,
            'model_loaded': self.model is not None,
            'tokenizer_loaded': self.tokenizer is not None
        }       
        
        
            # Ejemplo de uso
if __name__ == "__main__":
    print("="*60)
    print("TESTING LOGISTIC REGRESSION DETECTOR")
    print("="*60)
    
    # Crear detector LR
    detector = HateSpeechDetector()
    
    # Test individual
    test_text = "I hate you, you're so stupid!" 
    result = detector.predict(test_text)
    
    print("\n🔍 PREDICCIÓN INDIVIDUAL (LR):")
    print(f"Texto: {result['text']}")
    print(f"Predicción: {result['prediction']}")
    print(f"Confianza: {result['confidence']:.2%}")
    
    # Test batch
    test_texts = [
        "I love this video!",
        "You're an idiot, go die!",
        "Thanks for sharing this information"
    ]
    
    results = detector.predict_batch(test_texts)

    print("\n📊 PREDICCIÓN BATCH (LR):")
    for i, r in enumerate(results, 1):
        print(f"{i}. '{r['text'][:40]}...' → {r['prediction']} ({r['confidence']:.2%})")

    # Info del modelo
    print("\n📋 INFO DEL MODELO LR:")
    info = detector.get_model_info()
    for k, v in info.items():
        print(f"- {k}: {v}")
    
    print("\n" + "="*60)
    print("TESTING DISTILBERT DETECTOR")
    print("="*60)
    
    # Crear detector DistilBERT
    try:
        bert_detector = DistilBERTDetector()
        
        # Test individual
        result_bert = bert_detector.predict(test_text)
        
        print("\n🔍 PREDICCIÓN INDIVIDUAL (DistilBERT):")
        print(f"Texto: {result_bert['text']}")
        print(f"Predicción: {result_bert['prediction']}")
        print(f"Confianza: {result_bert['confidence']:.2%}")
        print(f"Probabilidades:")
        for label, prob in result_bert['probabilities'].items():
            print(f"  - {label}: {prob:.2%}")
        
        # Test batch
        results_bert = bert_detector.predict_batch(test_texts)
        
        print("\n📊 PREDICCIÓN BATCH (DistilBERT):")
        for i, r in enumerate(results_bert, 1):
            print(f"{i}. '{r['text'][:40]}...' → {r['prediction']} ({r['confidence']:.2%})")
        
        # Info del modelo
        print("\n📋 INFO DEL MODELO DISTILBERT:")
        info_bert = bert_detector.get_model_info()
        for k, v in info_bert.items():
            print(f"- {k}: {v}")
        
        # Comparación lado a lado
        print("\n" + "="*60)
        print("COMPARACIÓN LR vs DistilBERT")
        print("="*60)
        
        for i, text in enumerate(test_texts):
            lr_pred = results[i]
            bert_pred = results_bert[i]
            
            print(f"\nTexto {i+1}: '{text}'")
            print(f"  LR:   {lr_pred['prediction']:12} (conf: {lr_pred['confidence']:.2%})")
            print(f"  BERT: {bert_pred['prediction']:12} (conf: {bert_pred['confidence']:.2%})")
            
            if lr_pred['prediction'] != bert_pred['prediction']:
                print(f"  ⚠️  DESACUERDO entre modelos!")
    
    except Exception as e:
        print(f"\n❌ Error cargando DistilBERT: {e}")
        print("   Verifica que la carpeta 'distilbert-hate-speech' exista en backend/models/")
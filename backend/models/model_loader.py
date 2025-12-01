"""
Módulo para cargar y usar el modelo de detección de hate speech.
Utiliza Logistic Regression con threshold optimizado (0.3) y vectorizador TF-IDF.
"""

import pickle
import os
from pathlib import Path
import numpy as np
from backend.preprocessing.text_cleaner import full_preprocess


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
            'threshold_used': self.threshold
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

# Ejemplo de uso
if __name__ == "__main__":
    # Crear detector
    detector = HateSpeechDetector()
    
    # Test individual
    test_text = "I hate you, you're so stupid!" 
    result = detector.predict(test_text)
    
    print("\n🔍 PREDICCIÓN INDIVIDUAL:")
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

    print("\n📊 PREDICCIÓN BATCH:")
    for i, r in enumerate(results, 1):
        print(f"{i}. '{r['text'][:40]}...' → {r['prediction']} ({r['confidence']:.2%})")

    # Info del modelo
    print("\n📋 INFO DEL MODELO:")
    info = detector.get_model_info()
    for k, v in info.items():
        print(f"- {k}: {v}")            

    
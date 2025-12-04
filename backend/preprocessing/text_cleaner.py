import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

#Descargar recursos necesarios de NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    
def clean_text(text):
    """
    Normalizacion basica del texto
    
    Args:
    text (str): El texto a limpiar
    
    Returns:
        str: Texto limpio en minusculas, sin URLs, puntuacion ni numeros
    
    """
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)  # Eliminar URLs
    text = re.sub(r'[^\w\s]', '', text)  # Eliminar puntuacion
    text = re.sub(r'\d+', '', text)      # Eliminar numeros
    text = text.strip()
    return text

def preprocess_text(text):
    """
    Tokenizacion avanzada con NLTK: stopwords + stemming
    
    Args:
    text (str): Texto limpio (despues de clean_text)
    
    Returns:
        list: Tokens procesados (palabras stemmizadas sin stopwords
        
    """

    # Verificacion: Convertir a string y manejar casos vacios
    text = str(text).strip()
    if len(text) == 0:
        return []

    try: 
        # 1. Tokenización
        tokens = word_tokenize(text)
        
        # 2. Eliminación de stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        
        # 3. Stemming
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]
        
        return tokens

    except Exception as e:
        print(f"Error procesando texto '{text[:50]}...': {e}")
        return []

def full_preprocess(text):
    """
    Pipeline completo de preprocesamiento de texto
    
    Args:
    text (str): Texto original
    
    Returns:
        list: Tokens procesados (palabras stemmizadas sin stopwords)
    
    """
    # Paso 1: Limpieza del texto
    cleaned = clean_text(text)
    
    # Paso 2: Tokenizacion + Stopwords + Stemming
    tokens = preprocess_text(cleaned)
    
    # Paso 3: Unir tokens en string (necesario para TF-IDF)
    return ' '.join(tokens)

# Ejemplo de uso
if __name__ == "__main__":
    ejemplo = "I HATE you! You're so stupid 😡 http://spam.com"

    print("Original:", ejemplo)
    print("Limpio:", clean_text(ejemplo))
    print("Tokens:", preprocess_text(clean_text(ejemplo)))
    print("Final:", full_preprocess(ejemplo))
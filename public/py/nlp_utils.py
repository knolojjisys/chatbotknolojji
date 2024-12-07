import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def normalizar_pergunta(pergunta):
    """Normaliza uma pergunta para reduzir variações na forma de perguntar."""
    # Tokeniza a frase em palavras
    tokens = nltk.word_tokenize(pergunta)
    
    # Remove pontuações e converte para minúsculas
    tokens = [word.lower() for word in tokens if word.isalpha()]
    
    # Remove palavras comuns (stop words)
    tokens = [word for word in tokens if word not in stop_words]
    
    # Faz a lemmatização (reduz palavras para suas formas básicas)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Junta as palavras novamente em uma string
    return " ".join(tokens)

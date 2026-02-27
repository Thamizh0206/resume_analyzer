import re
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    """
    Basic text cleaning:
    - Lowercase
    - Remove special characters
    - Normalize spaces
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess_text(text: str) -> list:
    cleaned_text = clean_text(text)
    tokens = word_tokenize(cleaned_text)

    filtered_tokens = [
        token for token in tokens
        if token not in stop_words and len(token) > 2
    ]

    return filtered_tokens

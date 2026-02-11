
import nltk
from sentence_transformers import SentenceTransformer
import spacy.cli

def download_models():
    # Download NLTK data
    print("Downloading NLTK data...")
    nltk.download("punkt")
    nltk.download("punkt_tab")
    nltk.download("stopwords")

    # Download SpaCy model
    print("Downloading SpaCy model...")
    spacy.cli.download("en_core_web_sm")

    # Download Sentence Transformer model
    print("Downloading Sentence Transformer model...")
    SentenceTransformer("all-MiniLM-L6-v2")
    print("All models downloaded successfully.")

if __name__ == "__main__":
    download_models()

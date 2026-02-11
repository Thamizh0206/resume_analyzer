from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once (very important)
model = SentenceTransformer("all-MiniLM-L6-v2")

def embedding_similarity(resume_text: str, job_text: str) -> float:
    embeddings = model.encode([resume_text, job_text])

    resume_embedding = embeddings[0].reshape(1, -1)
    job_embedding = embeddings[1].reshape(1, -1)

    similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]

    return round(float(similarity * 100), 2)

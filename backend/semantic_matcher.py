import os
import numpy as np
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

def get_embedding(text):
    response = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    return response["embedding"]

def semantic_similarity(resume_text, job_text):

    resume_embedding = get_embedding(resume_text)
    job_embedding = get_embedding(job_text)

    similarity = cosine_similarity(resume_embedding, job_embedding)

    return round(similarity * 100, 2)

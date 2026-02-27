import os
import json
import hashlib
import numpy as np
from google import genai
import redis
from backend.logger import logger

# Configure Gemini with new SDK
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configure Redis
# Use REDIS_URL from environment variables (Render provides this)
redis_url = os.getenv("REDIS_URL")
redis_client = None

if redis_url:
    try:
        redis_client = redis.from_url(redis_url)
        # Test connection
        redis_client.ping()
        logger.info("Connected to Redis successfully")
    except Exception as e:
        logger.warning(f"Failed to connect to Redis: {e}. Caching disabled.")
        redis_client = None
else:
    logger.warning("REDIS_URL not found. Caching disabled.")

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

def get_embedding_key(text):
    """Generate a unique key for the text to use in Redis."""
    return f"embedding:{hashlib.sha256(text.encode()).hexdigest()}"

def get_embedding(text):
    if not text or not text.strip():
        return np.zeros(768) # Return zero vector or handle appropriately

    # 1. Check Cache
    if redis_client:
        key = get_embedding_key(text)
        try:
            cached_data = redis_client.get(key)
            if cached_data:
                logger.info("Cache Hit! Returning stored embedding.")
                return json.loads(cached_data)
        except Exception as e:
            logger.error(f"Redis read error: {e}")

    # 2. Call API if not in cache
    try:
        logger.info("Cache Miss. Calling Gemini API...")
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        embedding = response.embeddings[0].values

        # 3. Store in Cache
        if redis_client:
            try:
                # Store as JSON string, expire in 24 hours (86400 seconds) or keep indefinitely
                # Let's keep it for 7 days (604800 seconds) as embeddings don't change for same text
                redis_client.setex(key, 604800, json.dumps(embedding))
            except Exception as e:
                logger.error(f"Redis write error: {e}")

        return embedding
        
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        # Return a zero vector or re-raise depending on strictness. 
        # For now, let's re-raise to be safe.
        raise e

def semantic_similarity(resume_text, job_text):
    try:
        resume_embedding = get_embedding(resume_text)
        job_embedding = get_embedding(job_text)
        
        if resume_embedding is None or job_embedding is None:
            return 0.0

        similarity = cosine_similarity(resume_embedding, job_embedding)

        return round(similarity * 100, 2)
    except Exception as e:
        logger.error(f"Semantic similarity calculation failed: {e}")
        return 0.0

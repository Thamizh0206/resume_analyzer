import os
from dotenv import load_dotenv

load_dotenv()

WEIGHT_SKILL = float(os.getenv("WEIGHT_SKILL", 0.6))
WEIGHT_SEMANTIC = float(os.getenv("WEIGHT_SEMANTIC", 0.4))
WEIGHT_EMBEDDING = float(os.getenv("WEIGHT_EMBEDDING", 0.3))

def calculate_hybrid_score(skill_score, semantic_score, embedding_score):
    final_score = (
        (WEIGHT_SKILL * skill_score) +
        (WEIGHT_SEMANTIC * semantic_score) +
        (WEIGHT_EMBEDDING * embedding_score)
    )
    return round(final_score, 2)

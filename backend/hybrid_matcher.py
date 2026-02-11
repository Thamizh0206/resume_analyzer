import os
from dotenv import load_dotenv

load_dotenv()

WEIGHT_SKILL = float(os.getenv("WEIGHT_SKILL", 0.6))
WEIGHT_SEMANTIC = float(os.getenv("WEIGHT_SEMANTIC", 0.4))

def calculate_hybrid_score(skill_score, semantic_score):
    final_score = (WEIGHT_SKILL * skill_score) + (WEIGHT_SEMANTIC * semantic_score)
    return round(final_score, 2)

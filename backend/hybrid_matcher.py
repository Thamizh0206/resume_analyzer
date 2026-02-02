def calculate_hybrid_score(
    skill_match_percentage: float,
    semantic_match_percentage: float,
    skill_weight: float = 0.6,
    semantic_weight: float = 0.4
) -> float:
    """
    Combines rule-based skill match score and
    ML-based semantic similarity score into a final score.

    Weights must sum to 1.0
    """

    if skill_weight + semantic_weight != 1.0:
        raise ValueError("Skill weight and semantic weight must sum to 1.0")

    final_score = (
        skill_weight * skill_match_percentage
        + semantic_weight * semantic_match_percentage
    )

    return round(final_score, 2)

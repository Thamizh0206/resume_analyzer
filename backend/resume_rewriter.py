def generate_resume_improvements(
    resume_skills,
    job_skills,
    missing_skills
):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            f"Add a project or experience bullet highlighting hands-on usage of {skill}."
        )

    if "machine learning" in job_skills:
        suggestions.append(
            "Rewrite experience bullets to include ML impact metrics (accuracy, latency, scale)."
        )

    if "nlp" in job_skills:
        suggestions.append(
            "Mention NLP techniques explicitly (tokenization, embeddings, transformers)."
        )

    return suggestions

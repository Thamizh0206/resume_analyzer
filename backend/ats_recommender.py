def generate_ats_recommendations(
    resume_skills,
    job_skills,
    missing_skills,
    match_percentage
):
    recommendations = []

    if match_percentage < 50:
        recommendations.append(
            "Your resume has low alignment with the job description. Focus on adding core technical skills mentioned in the job."
        )

    if missing_skills:
        recommendations.append(
            f"Add these missing skills explicitly to your resume: {', '.join(missing_skills)}."
        )

    if "machine learning" in job_skills and "machine learning" not in resume_skills:
        recommendations.append(
            "Highlight machine learning projects with clear metrics and outcomes."
        )

    if match_percentage >= 75:
        recommendations.append(
            "Your resume is well-aligned. Minor refinements and stronger impact statements can improve shortlisting chances."
        )

    return recommendations

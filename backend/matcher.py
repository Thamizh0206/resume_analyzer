def calculate_match(resume_skills: list, job_skills: list) -> dict:
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    if not job_set:
        return {
            "match_percentage": 0.0,
            "common_skills": [],
            "missing_skills": []
        }

    common_skills = sorted(resume_set.intersection(job_set))
    missing_skills = sorted(job_set - resume_set)

    match_percentage = round(
        (len(common_skills) / len(job_set)) * 100, 2
    )
    
    return {
        "match_percentage": match_percentage,
        "common_skills": common_skills,
        "missing_skills": missing_skills
    }

import pandas as pd

def load_and_prepare_skills(skill_file_path: str) -> list:
    df = pd.read_csv(skill_file_path)

    prepared_skills = []
    for skill in df["skill"]:
        prepared_skills.append(skill.lower())

    return prepared_skills


def extract_skills(tokens: list, skill_list: list) -> list:
    found_skills = set()
    token_text = " ".join(tokens)

    for skill in skill_list:
        if skill in token_text:
            found_skills.add(skill)

    return sorted(found_skills)

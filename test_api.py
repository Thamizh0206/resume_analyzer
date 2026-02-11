import requests
import json
import time

url = "http://127.0.0.1:8000/final-match"
payload = {
    "resume_text": "Experienced Python Developer with strong background in machine learning, FastAPI, and Docker. Skilled in building RESTful APIs and NLP models.",
    "job_text": "We are looking for a Python Backend Engineer with experience in FastAPI, Docker, and Machine Learning. Knowledge of NLP is a plus."
}
headers = {"Content-Type": "application/json"}

for i in range(10):
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        print(json.dumps({
            "skill_match_percentage": data.get("skill_match_percentage"),
            "semantic_match_percentage": data.get("semantic_match_percentage"),
            "embedding_match_percentage": data.get("embedding_match_percentage"),
            "final_match_percentage": data.get("final_match_percentage")
        }, indent=2))
        break

    except Exception as e:
        print(f"Attempt {i+1}: Failed to connect ({e}). Retrying...")
        time.sleep(2)

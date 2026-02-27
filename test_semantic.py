import requests
import json

# Test the backend API
BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.json()}")
        return True
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return False

def test_semantic_match():
    """Test semantic matching endpoint"""
    try:
        data = {
            "resume_text": "Experienced Python developer with 5 years in machine learning and AI",
            "job_text": "Looking for a Python developer with ML experience"
        }
        
        response = requests.post(
            f"{BASE_URL}/semantic-match",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print("\nSemantic Match Test:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Semantic Match Score: {result.get('semantic_match_percentage', 0)}%")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Semantic Match Test Failed: {e}")

def test_final_match():
    """Test the full matching endpoint"""
    try:
        data = {
            "resume_text": "Python developer with expertise in FastAPI, machine learning, and data science. Skilled in TensorFlow and scikit-learn.",
            "job_text": "We need a Python developer with FastAPI and machine learning experience for our AI team."
        }
        
        response = requests.post(
            f"{BASE_URL}/final-match",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print("\nFinal Match Test:")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Skill Match: {result.get('skill_match_percentage', 0)}%")
            print(f"Semantic Match: {result.get('semantic_match_percentage', 0)}%")
            print(f"Final Score: {result.get('final_match_percentage', 0)}%")
            print(f"Confidence: {result.get('confidence', 'N/A')}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Final Match Test Failed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Resume Analyzer Backend")
    print("=" * 60)
    
    if test_health():
        print("\n" + "=" * 60)
        test_semantic_match()
        print("\n" + "=" * 60)
        test_final_match()
        print("\n" + "=" * 60)
        print("All tests completed!")
    else:
        print("Backend is not running. Please start it first.")

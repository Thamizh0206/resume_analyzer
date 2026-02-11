# FastAPI imports
from fastapi import FastAPI, Request, Body, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Core libs
import os
import shutil
import nltk

# Backend modules
from backend.text_preprocess import preprocess_text
from backend.skill_extractor import load_and_prepare_skills, extract_skills
from backend.matcher import calculate_match
from backend.semantic_matcher import semantic_similarity
from backend.hybrid_matcher import calculate_hybrid_score
from backend.resume_parser import extract_resume_text
from backend.ats_recommender import generate_ats_recommendations
from backend.resume_rewriter import generate_resume_improvements




# -------------------- NLTK SETUP --------------------

def setup_nltk():
    resources = [
        "punkt",
        "punkt_tab",
        "stopwords"
    ]

    for resource in resources:
        try:
            nltk.data.find(f"tokenizers/{resource}" if "punkt" in resource else f"corpora/{resource}")
        except LookupError:
            nltk.download(resource)


# -------------------- FASTAPI APP --------------------

app = FastAPI(title="AI Resume Analyzer API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend/dist/assets")),
    name="assets"
)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "frontend/dist")
)


'''
@app.on_event("startup")
def startup_event():
    setup_nltk()
'''

# -------------------- ROOT ENDPOINT --------------------

# @app.get("/")
# def read_root():
#     return {"status": "AI Resume Analyzer API is running"}


# -------------------- RESUME PARSING ENDPOINT --------------------

@app.post("/parse-resume")
def parse_resume(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDF and DOCX are supported."
        )

    temp_file_path = f"temp_{file.filename}"

    try:
        # Save uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract resume text
        text = extract_resume_text(temp_file_path)

        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail="Unable to extract text from the resume."
            )

        return {
            "filename": file.filename,
            "text_length": len(text),
            "text_preview": text[:500]
        }

    finally:
        # Always clean up temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/preprocess-text")
def preprocess_resume_text(text: str = Body(..., embed=True)):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Input text is empty")

    try:
        tokens = preprocess_text(text)
        return {
            "token_count": len(tokens),
            "tokens_preview": tokens[:30]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-skills")
def extract_resume_skills(text: str = Body(..., embed=True)):
    tokens = preprocess_text(text)

    prepared_skills = load_and_prepare_skills("data/skills.csv")
    extracted_skills = extract_skills(tokens, prepared_skills)

    return {
        "skill_count": len(extracted_skills),
        "skills": extracted_skills
    }

@app.post("/match-job")
def match_resume_to_job(
    resume_text: str = Body(..., embed=True),
    job_text: str = Body(..., embed=True)
):
    if not resume_text.strip() or not job_text.strip():
        raise HTTPException(status_code=400, detail="Resume or Job text is empty")

    # Resume processing
    resume_tokens = preprocess_text(resume_text)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SKILLS_PATH = os.path.join(BASE_DIR, "data", "skills.csv")
    skills_list = load_and_prepare_skills(SKILLS_PATH)
    resume_skills = extract_skills(resume_tokens, skills_list)

    # Job description processing
    job_tokens = preprocess_text(job_text)
    job_skills = extract_skills(job_tokens, skills_list)

    # Matching
    match_result = calculate_match(resume_skills, job_skills)

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "match_percentage": match_result["match_percentage"],
        "common_skills": match_result["common_skills"],
        "missing_skills": match_result["missing_skills"]
    }

@app.post("/semantic-match")
def semantic_match(
    resume_text: str = Body(..., embed=True),
    job_text: str = Body(..., embed=True)
):
    if not resume_text.strip() or not job_text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty")

    score = semantic_similarity(resume_text, job_text)

    return {
        "semantic_match_percentage": score
    }

@app.post("/final-match")
def final_match(
    resume_text: str = Body(..., embed=True),
    job_text: str = Body(..., embed=True)
):
    # Resume processing
    resume_tokens = preprocess_text(resume_text)
    skills_list = load_and_prepare_skills("data/skills.csv")
    resume_skills = extract_skills(resume_tokens, skills_list)

    # Job processing
    job_tokens = preprocess_text(job_text)
    job_skills = extract_skills(job_tokens, skills_list)

    # Skill-based matching
    match_result = calculate_match(resume_skills, job_skills)
    skill_match_percentage = match_result["match_percentage"]

    # Semantic matching
    semantic_match_percentage = semantic_similarity(resume_text, job_text)

    # Hybrid score
    final_score = calculate_hybrid_score(
        skill_match_percentage,
        semantic_match_percentage
    )

    recommendations = generate_ats_recommendations(
    resume_skills,
    job_skills,
    match_result["missing_skills"],
    final_score
)

    confidence = (
        "Strong" if final_score >= 75 else
        "Medium" if final_score >= 50 else
        "Weak"
    )
    rewrite_suggestions = generate_resume_improvements(
    resume_skills,
    job_skills,
    match_result["missing_skills"]
)



    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "skill_match_percentage": skill_match_percentage,
        "semantic_match_percentage": semantic_match_percentage,
        "final_match_percentage": final_score,
        "common_skills": match_result["common_skills"],
        "missing_skills": match_result["missing_skills"],
        "ats_recommendations": recommendations,
        "confidence": confidence,
        "rewrite_suggestions": rewrite_suggestions
    }

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

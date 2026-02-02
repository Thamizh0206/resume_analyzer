from fastapi import FastAPI, UploadFile, File, HTTPException
import nltk
import shutil
import os

from backend.resume_parser import extract_resume_text

# -------------------- NLTK SETUP --------------------

def setup_nltk():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")

    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")

# -------------------- FASTAPI APP --------------------

app = FastAPI(title="AI Resume Analyzer API")

@app.on_event("startup")
def startup_event():
    setup_nltk()

# -------------------- ROOT ENDPOINT --------------------

@app.get("/")
def read_root():
    return {"status": "AI Resume Analyzer API is running"}

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

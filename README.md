# AI Resume Analyzer

## Features
- Resume parsing (PDF/DOCX)
- Skill extraction (NLP based)
- Semantic similarity matching
- Hybrid weighted scoring
- FastAPI backend
- HTML/CSS frontend
- Dockerized deployment

## Run Locally

uvicorn backend.api:app --reload

## Docker

docker build -t ai-resume-analyzer .
docker run -d -p 8000:8000 ai-resume-analyzer

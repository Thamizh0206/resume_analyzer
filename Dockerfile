# Stage 1: Build the React frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy dependency definitions
COPY frontend/package.json frontend/package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the frontend source code
COPY frontend/ .

# Build the frontend application
RUN npm run build

# Stage 2: Serve with the backend
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for building C extensions or specialized libs)
# RUN apt-get update && apt-get install -y ...

COPY requirements.txt .

# Increase pip timeout and install python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --default-timeout=120 -r requirements.txt

# Download NLP models at build time
RUN python -m spacy download en_core_web_sm \
    && python - <<EOF
import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
EOF

# Copy backend code
COPY backend/ ./backend/
COPY data/ ./data/

# Copy built frontend assets from the builder stage
# We first ensure the destination directory exists
RUN mkdir -p frontend/dist

# Copy the build artifacts
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose the API port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]

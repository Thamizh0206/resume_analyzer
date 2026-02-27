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

# Create a non-root user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=user download_models.py .
RUN python download_models.py

COPY --chown=user backend/ ./backend/
COPY --chown=user data/ ./data/

RUN mkdir -p frontend/dist
COPY --chown=user --from=frontend-builder /app/frontend/dist ./frontend/dist

EXPOSE 7860

CMD ["python", "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "7860"]

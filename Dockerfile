# # Stage 1: Build React app
# FROM node:20 as frontend-builder

# WORKDIR /frontend
# COPY frontend/package*.json ./
# RUN npm install
# COPY frontend/ ./
# RUN npm run build

# Stage 2: Backend (FastAPI)
FROM python:3.11.13-slim

WORKDIR /app
COPY app/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY .env .env

# # Copy React build to FastAPI static path
# COPY --from=frontend-builder /frontend/build ./frontend/build

# Expose backend port
EXPOSE 8000

CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

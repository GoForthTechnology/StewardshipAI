# --- Stage 1: Build the Angular Frontend ---
FROM node:20-slim AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps
COPY frontend/ ./
# Tailwind v4 requires an explicit build step if the bundler integration fails
RUN npx @tailwindcss/cli -i src/styles.css -o src/styles.compiled.css
RUN npx ng build --configuration production

# --- Stage 2: Build the FastAPI Backend ---
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy the built frontend from Stage 1
COPY --from=frontend-build /app/frontend/dist/frontend/browser /app/static

# Expose port (Cloud Run default)
EXPOSE 8080

# Environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the application with Uvicorn
# We will serve static files from FastAPI in api.py
ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]

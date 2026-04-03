FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create required directories for ChromaDB and data
RUN mkdir -p data/chroma_db data/papers data/memory data/evaluations

# Expose ports (8000 for FastAPI, 8501 for Streamlit)
EXPOSE 8000 8501

# Default: Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


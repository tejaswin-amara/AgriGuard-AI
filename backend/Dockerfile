FROM python:3.12-slim

WORKDIR /app

# Install dependencies for psycopg2 and ml libraries
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code needed
COPY backend /app/backend
COPY models /app/models
COPY rag /app/rag

WORKDIR /app/backend
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# system dependencies for ML + fastText
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN mkdir -p /app/models

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY models/lid.176.ftz /app/models/
COPY run_pipeline.sh .

RUN useradd --create-home appuser && \
    chmod +x /app/run_pipeline.sh && \
    chown -R appuser:appuser /app

USER appuser

CMD ["bash", "run_pipeline.sh"]
FROM python:3.11-slim

WORKDIR /app

COPY services/ingest-api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/ingest-api/app ./app
COPY shared ./shared

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/shared

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

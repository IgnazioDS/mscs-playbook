FROM python:3.11-slim

WORKDIR /app

COPY services/worker/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/worker/app ./app
COPY shared ./shared

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/shared

CMD ["python", "-u", "app/worker.py"]

FROM python:3.11-slim

ARG APP_VERSION=dev
ARG APP_BUILD_SHA=local
ARG APP_BUILD_TIME=unknown

WORKDIR /app

COPY services/ingest-api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/ingest-api/app ./app
COPY shared ./shared

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/shared
ENV APP_VERSION=${APP_VERSION}
ENV APP_BUILD_SHA=${APP_BUILD_SHA}
ENV APP_BUILD_TIME=${APP_BUILD_TIME}

LABEL org.opencontainers.image.version=${APP_VERSION}
LABEL org.opencontainers.image.revision=${APP_BUILD_SHA}
LABEL org.opencontainers.image.created=${APP_BUILD_TIME}

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

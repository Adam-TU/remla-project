# Dockerfile needs to be built from root
FROM python:3.8.13-slim
WORKDIR /app/

COPY src/scraping_service/controller src/scraping_service/controller
COPY src/__init__.py src/gunicorn_config.py src/startup.sh src/

RUN apt-get update; apt-get install -y curl
RUN python -m pip install --upgrade pip && \
    python -m pip install -r src/scraping_service/controller/requirements.txt

EXPOSE 5000
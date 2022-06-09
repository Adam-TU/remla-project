# Dockerfile needs to be built from root
FROM python:3.8.13-slim
WORKDIR /app/

COPY src src

RUN apt-get update; apt-get install -y curl
RUN python -m pip install --upgrade pip && \
    python -m pip install -r src/scraper/controller/requirements.txt
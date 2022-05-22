FROM python:3.8-alpine
WORKDIR  /app
COPY Makefile /app/Makefile
COPY requirements.txt /app/requirements.txt
RUN apk add --update make
RUN python -m make requirements
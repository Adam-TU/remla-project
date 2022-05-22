FROM python:3.8-alpine
WORKDIR  /app
COPY Makefile /app/
COPY requirements.txt /app/
COPY test_environment.py /app/
RUN apk add --update make
RUN make requirements
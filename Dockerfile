FROM python:3.8-slim
WORKDIR  /app
COPY Makefile /app/
COPY requirements.txt /app/
COPY test_environment.py /app/
COPY pyproject.toml /app/
COPY setup.py /app/
RUN apk add --update make
RUN make requirements
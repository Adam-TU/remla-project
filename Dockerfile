FROM python:3.8-slim
WORKDIR  /app

COPY Makefile /app/
COPY requirements.txt /app/
COPY test_environment.py /app/
COPY pyproject.toml /app/
COPY setup.py /app/

RUN apt-get update
RUN apt-get -y install make
RUN make requirements
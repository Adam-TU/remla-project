FROM python:3.8-slim
WORKDIR  /app

COPY Makefile /app/
COPY requirements.txt /app/
COPY test_environment.py /app/
COPY pyproject.toml /app/
COPY setup.py /app/

RUN sudo apt-get update
RUN sudo apt-get -y install make
RUN make requirements
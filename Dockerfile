FROM python:3.8-alpine
RUN python -m pip install make
COPY Makefile .
COPY requirements.txt .
RUN python -m make requirements
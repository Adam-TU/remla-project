FROM python:3.8-alpine
COPY Makefile .
COPY requirements.txt .
RUN ls
RUN python -m pip install make
RUN python -m make requirements
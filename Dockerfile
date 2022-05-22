FROM python:3.8-alpine
WORKDIR  /app
COPY Makefile /app/Makefile
COPY requirements.txt /app/requirements.txt
RUN ls
RUN python -m pip install make
RUN python -m make requirements
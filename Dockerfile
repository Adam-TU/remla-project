FROM python:3.8-alpine
RUN python -m pip install make
RUN python -m make requirements
# syntax=docker/dockerfile:1
FROM python:3.8.13-slim

WORKDIR /root/

COPY requirements.txt .

COPY src src
COPY data data
COPY reports reports

RUN python -m pip install --upgrade pip &&\
    pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["src/serve_model.py"]

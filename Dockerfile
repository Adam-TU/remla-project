FROM python:3.8.13-slim AS model_build

WORKDIR /root/

COPY requirements.txt pyproject.toml setup.py ./

RUN python -m pip install --upgrade pip &&\
    python -m pip install -r requirements.txt

COPY src src
COPY services-shared-folder/data data
COPY reports reports

COPY params.yaml dvc.yaml ./

RUN mkdir models &&\
 dvc init --no-scm &&\
 dvc repro

FROM python:3.8.13-slim

WORKDIR /root/

RUN mkdir models
COPY --from=model_build /root/models models

COPY src src

COPY requirements.txt params.yaml pyproject.toml setup.py ./

RUN python -m pip install --upgrade pip &&\
 python -m pip install -r src/requirements.txt

EXPOSE 5000
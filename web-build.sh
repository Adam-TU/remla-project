#!/bin/sh

cd web-frontend/myweb

docker build -t web-frontend .

cd ../..

docker build -t inference-api .

docker-compose up

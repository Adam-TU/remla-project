FROM python:3.8.13-buster

WORKDIR /root/

RUN pip --upgrade pip && pip install -r requirements.txt
COPY ./* .

ENTRYPOINT [ "python" ]
CMD [ "scraper.py" ]

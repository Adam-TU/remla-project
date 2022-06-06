FROM python:3.8.13-buster

WORKDIR /root/

RUN pip install pandas
RUN pip install requests
RUN pip install tensorflow_data_validation

COPY scraper.py .
COPY data_validation.py .
COPY train.tsv .

ENTRYPOINT [ "python" ]
CMD [ "scraper.py" ]

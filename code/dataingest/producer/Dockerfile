FROM python:3.6-alpine
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY producer.py ./scripts/
COPY sample.csv ./data/

RUN pip install -r requirements.txt
RUN chmod +x scripts/producer.py
CMD python scripts/producer.py
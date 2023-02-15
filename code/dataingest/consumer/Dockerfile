FROM python:3.6-alpine
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY consumer.py ./scripts/

RUN pip install -r requirements.txt
RUN chmod +x scripts/consumer.py
CMD python scripts/consumer.py
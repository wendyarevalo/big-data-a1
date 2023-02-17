FROM python:3.6-alpine
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY insertion_test.py ./scripts/
COPY sample.csv ./data/

RUN pip install -r requirements.txt
RUN chmod +x scripts/insertion_test.py
CMD python scripts/insertion_test.py
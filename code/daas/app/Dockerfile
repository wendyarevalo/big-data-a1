FROM python:3.6-alpine
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY . ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]
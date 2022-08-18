FROM python:slim

RUN pip install sklearn mlflow matplotlib boto3

COPY train.py .
COPY predict.py .

ENTRYPOINT ["python"]

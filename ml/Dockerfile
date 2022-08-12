FROM python:slim

RUN pip install sklearn

COPY train.py .
COPY predict.py .

ENTRYPOINT ["python"]

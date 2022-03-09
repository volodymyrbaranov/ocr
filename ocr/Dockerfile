FROM python:3.9-slim

WORKDIR /ocr

RUN apt-get update && apt-get install -y python3-opencv libleptonica-dev tesseract-ocr libtesseract-dev tesseract-ocr-rus

COPY requirements.txt requirements.txt

RUN pip install -U pip

RUN pip install -r requirements.txt

ENV FLASK_APP=server
COPY . .
EXPOSE 5001

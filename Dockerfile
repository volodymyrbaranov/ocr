FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y python3-opencv libleptonica-dev tesseract-ocr libtesseract-dev tesseract-ocr-rus

RUN pip install -U pip

COPY . .

RUN pip install -r requirements.txt

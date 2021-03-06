import re
from enum import Enum

import pytesseract
import numpy as np
import cv2
from paddleocr import PaddleOCR

from google import extract_text as google_extract_text

PADDLE_OCR = PaddleOCR(use_angle_cls=True, lang="ru")


class RecognizeType(str, Enum):
    TESSERACT = "tesseract"
    PADDLE = "paddle"
    GOOGLE = "google"


def bytes2cv2(b):
    np_array = np.fromstring(b, np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_ANYCOLOR)


def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    return invert


def postprocess_text(text):
    text = re.sub(' +', ' ', text)
    text = text.replace('\f', '')
    text = re.sub('(\d{2}\:\d{2})', '', text)
    return text


def paddle_ocr_recognize(b):
    img = bytes2cv2(b)
    lines = PADDLE_OCR.ocr(img, cls=True)
    words = [line[-1][1] for line in lines]
    return " ".join(words)


def get_text(b, ocr_type=RecognizeType.TESSERACT.value):
    if ocr_type == RecognizeType.TESSERACT.value:
        img = bytes2cv2(b)
        img = preprocess(img)
        text = pytesseract.image_to_string(img, lang="rus")
        text = postprocess_text(text).strip()
    elif ocr_type == RecognizeType.PADDLE.value:
        text = paddle_ocr_recognize(b)
    elif ocr_type == RecognizeType.GOOGLE.value:
        text = google_extract_text(b)
    return text

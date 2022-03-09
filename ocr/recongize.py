import pytesseract
import numpy as np
import cv2


def bytes2cv2(b):
    np_array = np.fromstring(b, np.uint8)
    return cv2.imdecode(np_array, cv2.IMREAD_COLOR)


def preprocess(image):
    if len(np.array(image).shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    return invert


def get_text(b):
    img = bytes2cv2(b)
    img = preprocess(img)
    text = pytesseract.image_to_string(img, lang="rus")
    return text.strip()

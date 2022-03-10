import base64
import os
import json

import requests

API_ROOT = "https://vision.googleapis.com"

API_KEY = os.getenv("GOOGLE_OCR_API_KEY")
if not API_KEY:
    raise AttributeError("Google API_KEY not found")


def _annotate_image(b):

    content = base64.b64encode(b)
    image = {
        "content": str(content, "utf-8")
    }

    body = {
        "requests": {
            "image": image,
            "features": {"type": "TEXT_DETECTION"}
        }
    }

    data = json.dumps(body).encode()

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        url=f"{API_ROOT}/v1/images:annotate?key={API_KEY}",
        headers=headers,
        data=data,
        timeout=10,
    )

    annotation = response.json()
    return annotation


def extract_text(b):
    annotation = _annotate_image(b)
    responses = annotation["responses"]
    response = responses[0]["textAnnotations"][0]
    return response["description"].strip()


__all__ = [
    "extract_text",
]

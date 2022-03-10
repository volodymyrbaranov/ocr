from ocr import app

from .recongize import get_text

from flask import request, jsonify

ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/health/", methods=["GET"])
def health():
    return jsonify({"health": "ok"})


@app.route("/extract_text/<ocr>", methods=["POST"])
def extract_text(ocr):
    file = request.files["file"]
    image = file.read()
    text = get_text(image, ocr)
    return jsonify(
        {"text": text}
    )

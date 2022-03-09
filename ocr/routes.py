from recongize import get_text
from flask import request, jsonify
from logging.config import dictConfig
from flask import Flask

dictConfig({
    "version": 1,
    "formatters": {"default": {
        "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    }},
    "handlers": {"wsgi": {
        "class": "logging.StreamHandler",
        "stream": "ext://flask.logging.wsgi_errors_stream",
        "formatter": "default"
    }},
    "root": {
        "level": "INFO",
        "handlers": ["wsgi"]
    }
})

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/health/", methods=["GET"])
def health():
    return jsonify({"health": "ok"})


@app.route("/extract_text/", methods=["POST"])
def extract_text():
    print('asd')
    file = request.files["image"]
    filename = file.filename
    if not allowed_file(filename):
        return "Not allowed file", 400
    image_id = filename.rsplit(".", 1)[0]
    app.logger.info(f"Recognize image {image_id}")
    image = file.read()
    text = get_text(image)
    return jsonify(
        {"text": text}
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)

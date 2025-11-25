import os
import re
import tempfile
from io import BytesIO
from flask import Flask, request, jsonify

from pdfminer.high_level import extract_text


EMAIL_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+", re.IGNORECASE)
PHONE_REGEX = re.compile(r"(?:\+?\d{1,3}[ -]?)?(?:\(?\d{3}\)?[ -]?)?\d{3}[ -]?\d{4}")


def parse_resume(file_stream: BytesIO) -> dict:
    """Extract basic fields from a PDF resume."""
    # Write the file to a temporary location
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file_stream.read())
        tmp_path = tmp.name

    try:
        text = extract_text(tmp_path)
    finally:
        os.unlink(tmp_path)
    # Use simple heuristics for name: assume the first line contains the name
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name = lines[0] if lines else None
    emails = EMAIL_REGEX.findall(text)
    phones = PHONE_REGEX.findall(text)
    return {
        "name": name,
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "raw_text": text[:5000],  # return first 5k characters for debugging
    }


def create_app():
    """Create Flask app for resume parsing."""
    app = Flask(__name__)

    @app.route("/parse", methods=["POST"])
    def parse_endpoint():
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400
        parsed = parse_resume(file.stream)
        return jsonify(parsed)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "resume-parser-service up"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5004, debug=True)
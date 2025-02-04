from flask import Flask, request, jsonify
import pytesseract
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Set Tesseract path (update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def process_image(image_data, preserve_line_breaks):
    """ Convert base64 image to text using Tesseract OCR """
    # Decode base64
    image_bytes = base64.b64decode(image_data)
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Perform OCR
    extracted_text = pytesseract.image_to_string(gray)

    if not preserve_line_breaks:
        # Replace newlines with spaces and clean extra spaces
        extracted_text = " ".join(extracted_text.split())

    return extracted_text

@app.route("/ocr", methods=["POST"])
def ocr_endpoint():
    try:
        data = request.json
        base64_image = data.get("image")
        preserve_line_breaks = data.get("preserve_line_breaks", True)  # Default: preserve line breaks

        if not base64_image:
            return jsonify({"error": "No image data provided"}), 400

        text = process_image(base64_image, preserve_line_breaks)
        return jsonify({"extracted_text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Flask OCR API is running on http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)

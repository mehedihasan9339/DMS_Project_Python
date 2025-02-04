# OCR API with Flask, Tesseract OCR, and OpenCV

This project provides a step-by-step guide to creating and running an Optical Character Recognition (OCR) API using Flask, Tesseract OCR, and OpenCV on a Windows PC with Visual Studio Code (VS Code). The API accepts a base64-encoded image, processes it using Tesseract OCR, and returns the extracted text.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
   - [Step 1: Install Tesseract OCR](#step-1-install-tesseract-ocr)
   - [Step 2: Set Up Environment Variable for Tesseract](#step-2-set-up-environment-variable-for-tesseract)
   - [Step 3: Install Python and Required Libraries](#step-3-install-python-and-required-libraries)
3. [Set Up Flask Application](#set-up-flask-application)
   - [Step 4: Create `ocr_api.py`](#step-4-create-ocr_apypy)
4. [Run the Flask API](#run-the-flask-api)
   - [Step 5: Run the Flask API](#step-5-run-the-flask-api)
5. [Test the OCR API](#test-the-ocr-api)
   - [Step 6: Test Using Postman or cURL](#step-6-test-using-postman-or-curl)
6. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
7. [Summary](#summary)

---

## Prerequisites

Before starting, ensure you have the following installed:

- **Python**: Download and install Python from [python.org](https://www.python.org/).
- **VS Code**: Install Visual Studio Code from [code.visualstudio.com](https://code.visualstudio.com/).
- **Tesseract OCR**: Download and install Tesseract OCR for Windows from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).

---

## Installation

### Step 1: Install Tesseract OCR

1. Download the Tesseract installer for Windows from [this link](https://github.com/tesseract-ocr/tesseract).
2. Run the installer and follow the instructions. The default installation directory is usually:
3. Remember the installation path, as you will need to reference it in your code.

---

### Step 2: Set Up Environment Variable for Tesseract

1. Open **System Properties**:
- Right-click on **This PC** > **Properties** > **Advanced system settings**.
2. Click on **Environment Variables**.
3. Under **System variables**, find and select **Path**, then click **Edit**.
4. Add the path to the Tesseract installation (e.g., `C:\Program Files\Tesseract-OCR`).
5. Click **OK** to save the changes.
6. Restart your PC to ensure the environment variable is loaded.

---

### Step 3: Install Python and Required Libraries

1. **Install Python**:
- Ensure Python is installed and available in your command prompt by running:
  ```bash
  python --version
  ```
- If not installed, download and install it from the [Python website](https://www.python.org/).

2. **Install Required Python Libraries**:
- Open a terminal in VS Code and install the necessary libraries:
  ```bash
  pip install flask pytesseract opencv-python numpy
  ```

---

## Set Up Flask Application

### Step 4: Create `ocr_api.py`

1. Open VS Code and create a new Python file named `ocr_api.py`.
2. Copy and paste the following code into the file:

```python
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
 ```
 
 ## Run the Flask API

### Step 5: Run the Flask API

1. Open the terminal in VS Code (or any terminal).
2. Navigate to the directory where `ocr_api.py` is located.
3. Run the Flask API by typing:
   ```bash
   python ocr_api.py
   ```
4. If everything is set up correctly, you should see the following output:
    ```
    🚀 Flask OCR API is running on http://127.0.0.1:5000
    ```

## Step 6: Test the OCR API

### Using Postman:

1. Open Postman and create a new `POST` request.
2. Set the URL to `http://127.0.0.1:5000/ocr`.
3. In the **Body** tab, select **raw** and set the format to **JSON**.
4. Include the following JSON body:

   ```json
   {
       "image": "<base64-encoded-image>",
       "preserve_line_breaks": true
   }
   ```

### Sample Response:

```json
{
    "extracted_text": "This is just to say\n\nI have eaten\nthe plums\nthat were in\nthe icebox\n\nand which\n\nyou were probably\nsaving\n\nfor breakfast\n\nForgive me\n\nthey were delicious\nso sweet\n\nand so cold\n\nWilliam Carlos Williams\n(September 17th 1883 — March 4th 1963)\n"
}
```


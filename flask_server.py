from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    # filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    # file.save(filepath)
    return jsonify({"message": "File uploaded successfully"}), 200

if __name__ == "__main__":
    app.run(port=5000)
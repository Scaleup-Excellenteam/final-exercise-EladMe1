import os
import time
import uuid
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/upload",methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"message": "No file uploaded."}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"message": "No file selected."}), 400

        if file and allowed_file(file.filename):
            # Generate a unique identifier (UID) for the file
            uid = str(uuid.uuid4())

            # Get the original filename and file extension
            original_filename = file.filename
            _, extension = os.path.splitext(original_filename)

            # Generate a timestamp for the file upload
            timestamp = int(time.time())

            # Generate the new filename with original filename, timestamp, and UID
            new_filename = f"{original_filename}_{timestamp}_{uid}{extension}"

            # Save the uploaded file to the "uploads" directory with the new filename
            file_path = os.path.join("uploads", new_filename)
            file.save(file_path)

            # Return the UID in a JSON response
            return jsonify({"uid": uid}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


def allowed_file(filename):
    # Check if the file has a valid extension (.pptx)
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pptx"


if __name__ == '__main__':
    app.run()

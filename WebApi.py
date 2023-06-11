import json
import os
import re
import uuid

from datetime import datetime
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')


@app.route("/", methods=["GET"])
def index():
    """
       Home page route.
       """
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
     Upload route to handle file uploads.

     Returns:
         JSON: JSON response with the UID of the uploaded file.
     """
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
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

            # Generate the new filename with original filename, timestamp, and UID
            new_filename = f"{original_filename}_{timestamp}_{uid}{extension}"

            # Save the uploaded file to the "uploads" directory with the new filename
            file_path = os.path.join("uploads", new_filename)
            file.save(file_path)

            # Return the UID in a JSON response
            return jsonify({"uid": uid}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@app.route("/check_file", methods=["GET", "POST"])
def check_file():
    """
      Check the status of a file route.

      Returns:
          JSON: JSON response with the status, filename, timestamp, and explanation of the file.
      """
    try:
        uid = request.args.get("uid")
        if uid:
            done_success, done_data = is_done(uid)

            if done_success:
                return jsonify(done_data), 200

            pending_success, pending_data = is_pending(uid)
            if pending_success:
                return jsonify(pending_data), 200

        return jsonify({"message": f"No file with UID {uid} found."}), 404

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


def is_done(uid):
    """
      Check if a file with the given UID is done processing.

      Args:
          uid (str): The UID of the file.

      Returns:
          tuple: A tuple indicating if the file is done processing (bool) and the file data (dict).
      """
    files = os.listdir('outputs')
    for file in files:
        if uid in file:
            original_filename = extract_filename(file)
            timestamp = extract_timestamp(file)
            explanation = get_explanation(uid)
            return True, {
                "status": "done",
                "filename": original_filename,
                "timestamp": timestamp,
                "explanation": explanation
            }
    return False, {}  # File not found, return False and an empty dictionary


def get_explanation(uid):
    """
       Get the explanation for a file with the given UID.

       Args:
           uid (str): The UID of the file.

       Returns:
           dict or None: The explanation data as a dictionary, or None if the file is not found.
       """
    files = os.listdir('outputs')
    for file in files:
        if uid in file:
            with open(os.path.join('outputs', file), 'r') as f:
                json_data = f.read()
                data = json.loads(json_data)
                return data
    return None


def extract_filename(file):
    """
     Extract the original filename from the processed file.

     Args:
         file (str): The filename.

     Returns:
         str: The original filename.
     """
    filename_parts = file.split("_", 1)
    original_filename = filename_parts[0]
    return original_filename


def extract_timestamp(file):
    """
       Extract the timestamp from the processed file.

       Args:
           file (str): The filename.

       Returns:
           str: The formatted timestamp.
       """
    timestamp_match = re.search(r"_(\d{14})", file)
    timestamp = ""
    if timestamp_match:
        timestamp = timestamp_match.group(1)
    return format_timestamp(timestamp)


def is_pending(uid):
    """
    Check if a file with the given UID is still pending.

    Args:
        uid (str): The UID of the file.

    Returns:
        tuple: A tuple indicating if the file is pending (bool) and the file data (dict).
    """
    files = os.listdir('uploads') + os.listdir('pending')
    for file in files:
        if uid in file:
            original_filename = extract_filename(file)
            timestamp = extract_timestamp(file)
            return True, {
                "status": "pending",
                "filename": original_filename,
                "timestamp": timestamp,
                "explanation": "None"
            }
    return False, {}


def format_timestamp(timestamp):
    """
       Format the timestamp into a human-readable format.

       Args:
           timestamp (str): The timestamp string.

       Returns:
           str: The formatted timestamp string.
       """
    year = timestamp[:4]
    month = timestamp[4:6]
    day = timestamp[6:8]
    hour = timestamp[8:10]
    minute = timestamp[10:12]
    second = timestamp[12:14]

    formatted_timestamp = f"Upload Date: {day}/{month}/{year} at {hour}:{minute}:{second}"
    return formatted_timestamp


def allowed_file(filename):
    """
      Check if the filename has a valid extension.

      Args:
          filename (str): The filename.

      Returns:
          bool: True if the filename has a valid extension, False otherwise.
      """
    # Check if the file has a valid extension (.pptx)
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "pptx"


if __name__ == '__main__':
    app.run()

import os
import uuid

from flask import Flask, render_template, request
from google.cloud import storage
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set this as an environment variable, or replace with a hard-coded bucket name.
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "bkt-sales-data-px")

def upload_file_to_gcs(file_storage, bucket_name: str) -> str:
    """
    Uploads a Werkzeug FileStorage object to GCS.
    Returns the uploaded object name (path) in the bucket.
    """
    if not bucket_name:
        raise RuntimeError("GCS_BUCKET_NAME is not set.")

    # Create a safe filename and make it unique
    safe_name = secure_filename(file_storage.filename)
    if not safe_name:
        raise ValueError("Invalid filename.")

    object_name = f"uploads/{uuid.uuid4().hex}-{safe_name}"

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    # Upload directly from the request stream
    blob.upload_from_file(
        file_storage.stream,
        content_type=file_storage.mimetype,
        rewind=True,  # ensures stream is read from the start
    )

    return object_name

@app.get("/")
def index():
    return render_template("index.html", message=None, success=True)

@app.post("/upload")
def upload():
    try:
        if "file" not in request.files:
            return render_template("index.html", message="No file part in the request.", success=False), 400

        f = request.files["file"]
        if not f or f.filename == "":
            return render_template("index.html", message="No file selected.", success=False), 400

        object_name = upload_file_to_gcs(f, GCS_BUCKET_NAME)

        return render_template(
            "index.html",
            message=f"✅ Uploaded successfully to gs://{GCS_BUCKET_NAME}/{object_name}",
            success=True,
        )

    except Exception as e:
        return render_template("index.html", message=f"❌ Upload failed: {e}", success=False), 500

if __name__ == "__main__":
    # For local dev only. In production, use gunicorn.
    app.run(host="0.0.0.0", port=8080, debug=True)

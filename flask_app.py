from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from assistant import NotesAssistant

app = Flask(__name__)

UPLOAD_FOLDER = "/path/to/the/upload/directory"
ALLOWED_EXTENSIONS = {"mp4"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            notes_assistant = NotesAssistant(
                os.path.join(app.config["UPLOAD_FOLDER"], filename)
            )
            notes_assistant.make_notes()
            return "Notion page created successfully!"
    return """
    <!doctype html>
    <title>Upload new Video File</title>
    <h1>Upload new Video File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


if __name__ == "__main__":
    app.run(debug=True)

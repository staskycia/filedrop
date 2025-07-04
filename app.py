import os
from flask import Flask, render_template, url_for,  request, flash, get_flashed_messages, abort
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png'}

def allowed_file(filename):
    return "." in filename and filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config["SECRET_KEY"] = "alamakota"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("upload.html")
        uploaded = request.files.getlist("file")
        # no attachments
        if(uploaded[0].filename == ""):
            flash("No files to drop!")
            return render_template("upload.html")
        
        for file in uploaded:
            if file and allowed_file(file.filename):
                filename = f'FILEDROP_{str(datetime.now()).replace(" ", "_")}_{secure_filename(file.filename).replace(" ", "_")}'
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            elif file:
                abort(400, "File type not allowed")
                flash("Unable to drop '" + file.filename + "'!")

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)
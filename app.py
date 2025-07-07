import os
from flask import Flask, render_template, url_for,  request, flash, get_flashed_messages, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from random import randint
from consolewindow import console_window

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png'}

def allowed_file(filename):
    return "." in filename and filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config["SECRET_KEY"] = "alamakota"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "filedrop.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please login to acces the panel!"
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    
with app.app_context():
    db.create_all()
    
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

def change_password(username, new_password):
    with app.app_context():
        user = User.query.filter_by(username = username).first()
        user.password = generate_password_hash(new_password)
        db.session.commit()

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

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if not password:
            flash("Password is required!")
            return render_template("login.html")
        adminuser = User.query.filter_by(username = "admin").first()
        if check_password_hash(adminuser.password, password):
            login_user(adminuser, remember=True)
            return redirect(url_for("panel"))
        else:
            flash("Password incorrect!")
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/panel")
@login_required
def panel():
    return f"PANEL of user {current_user.username} USING {request.remote_addr}"

@app.route("/recovery", methods=["POST", "GET"])
def recovery():
    if request.method == "POST" and request.remote_addr == "127.0.0.1":
        new_password = f"{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}-{randint(1000, 9999)}"
        change_password("admin", new_password)
        console_window("NEW FILEDROP PANEL PASSWORD", new_password)
        flash("Password changed succesfully! Check the console for details.")
        return redirect(url_for("login"))
    return render_template("recovery.html", allowed = True if request.remote_addr == "127.0.0.1" else False)
   

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)
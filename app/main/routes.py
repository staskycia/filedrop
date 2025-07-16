from flask import render_template, request, flash, abort, redirect, url_for, current_app, send_file
from flask_login import login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from random import randint

from app.models.user import User
from app.extensions import db
from app.config_tools import get_config, allowed_file, get_whitelist_status, get_blacklist_status

from app.main import bp

def console_window(title, content):
    title = str(title)
    content = str(content)
    print(f"""
{"#" * 40}
{"#" * int((38 - len(title))/2)} {title} {"#" * int((38 - len(title))/2 + (1 if len(title) % 2 == 1 else 0))}
{"#" * 40}
#{" "*38}#
#{" "*38}#
#{" " * int((38 - len(content))/2)}{content}{" " * int((38 - len(content))/2 + (1 if len(content) % 2 == 1 else 0))}#
#{" "*38}#
#{" "*38}#
{"#" * 40}
""")

@bp.route("/")
@bp.route("/upload", methods=["POST", "GET"])
def upload():   
    flash("Since this is a demo instance, you can find all shared files at <a href='/files' class='text-yellow-800 hover:text-yellow-900'>/files</a>. See the <a href='https://vimeo.com/1101557107?ts=0&share=copy' class='text-yellow-800 hover:text-yellow-900'>demo video</a> for details ans <a href='https://github.com/staskycia/filedrop' class='text-yellow-800 hover:text-yellow-900'>GitHub</a> for installation guide.", "warning")
    security_mode = get_config("security_mode")
    user_ip = request.remote_addr
    if security_mode != "none":
        if (security_mode == "whitelist" and get_whitelist_status(user_ip) == 0) or (security_mode == "blacklist" and get_blacklist_status(user_ip) == 1):
            if request.method == "POST":
                abort(403, "Not allowed!")
            return render_template("upload.html", enabled=False)
    enabled = True if get_config("sharing_enabled") == "True" else False
    print(1 if enabled else 0)
    if request.method == "POST":
        if not enabled:
            abort(400, "Sharing not enabled!")
            current_app.logger.info(f"{request.remote_addr} tried to share files, but this option is not enabled")
        if "file" not in request.files:
            return render_template("upload.html", enabled=enabled)
        uploaded = request.files.getlist("file")
        # no attachments
        if(uploaded[0].filename == ""):
            current_app.logger.info(f"{request.remote_addr} sent no files")
            flash("No files to drop!", "error")
            return render_template("upload.html", enabled=enabled)
        
        for file in uploaded:
            if file and allowed_file(file.filename):
                filename = f'FILEDROP_{str(datetime.now()).replace(" ", "_").replace(":", "_")}_{secure_filename(file.filename).replace(" ", "_")}'
                current_app.logger.info(f'{request.remote_addr} succesfully shared file "{filename}"')
                file.save(os.path.join(get_config("upload_folder"), filename))
            elif file:
                current_app.logger.info(f"{request.remote_addr} tried to send file that is not allowed ({file.filename.split(".")[-1]})")
                abort(400, "File type not allowed")
                flash("Unable to drop '" + file.filename + "'!", "error")
    return render_template("upload.html", enabled=enabled)

@bp.route("/login", methods=["POST", "GET"])
def login():
    flash("This is a demo instance, so you may use password \"<strong>admin</strong>\"", "warning")
    if current_user.is_authenticated:
        return redirect("panel")
    if request.method == "POST":
        password = request.form.get("password")
        if not password:
            flash("Password is required!", "error")
            return render_template("login.html")
        adminuser = User.query.filter_by(username = "admin").first()
        if check_password_hash(adminuser.password, password):
            login_user(adminuser, remember=True)
            current_app.logger.info(f"{request.remote_addr} succesfully logged in to the panel")
            return redirect(url_for("panel.configuration"))
        else:
            current_app.logger.info(f"{request.remote_addr} tried to log in with wrong password")
            flash("Password incorrect!", "error")
    return render_template("login.html")

@bp.route("/logout")
def logout():
    logout_user()
    current_app.logger.info(f"{request.remote_addr} logged out")
    flash("You were securely logged out!", "success")
    return redirect(url_for("main.login"))

@bp.route("/recovery", methods=["POST", "GET"])
def recovery():
    if request.method == "POST" and request.remote_addr == "127.0.0.1":
        logout_user()
        flash("Your new password is \"<strong>admin</strong>\"", "success")
        return redirect(url_for("main.login"))
    else:
        flash("Usually, this option is only available on the host computer", "warning")
    return render_template("recovery.html", allowed = True)

@bp.route("/files")
def files():
    flash("This is a demo-only feature!", "warning")
    return render_template("/files.html", files=os.listdir(get_config("upload_folder")))

@bp.route("/file/<file>")
def fileviewer(file):
    file_path = os.path.join(get_config("upload_folder"), file)
    if os.path.exists(file_path):
        return send_file(file_path)
    flash("Requested file wasn't found!", "error")
    return redirect(url_for("main.files"))
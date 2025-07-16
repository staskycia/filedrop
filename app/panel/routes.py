from flask import render_template, request, flash, current_app, Response
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash

import os
import markdown
import psutil
import socket
import base64
import qrcode
from io import BytesIO

from app.models.user import User
from app.extensions import db
from app.config_tools import get_config, set_config, get_all_extensions, set_extension_status, add_extension, delete_extension, add_ip, delete_ip, get_all_ips, set_whitelist_status, set_blacklist_status

from app.panel import bp


def get_host_ips():
    ips = set()
    for iface_info in psutil.net_if_addrs().values():
        for addr in iface_info:
            if addr.family == socket.AF_INET and not addr.address.startswith("169.254"):
                ips.add(addr.address)

    return sorted(ips)

def get_port():
    return request.host.split(":")[-1]
    
@bp.route("/", methods=["POST", "GET"])
@bp.route("/configuration", methods=["POST", "GET"])
@login_required
def configuration():
    flash("This is a demo instance, so some setting may not be available", "warning")
    sharing_enabled = True if get_config("sharing_enabled") == "True" else False
    if request.method == "POST":
        field = request.form.get("field")
        if field == "sharing_action":
            sharing_action = request.form.get("sharing_action")
            if sharing_action == "disable":
                set_config("sharing_enabled", "False")
                current_app.logger.info(f"{request.remote_addr} disabled file sharing")
            else:
                set_config("sharing_enabled", "True")
                current_app.logger.info(f"{request.remote_addr} enabled file sharing")
            sharing_enabled = True if get_config("sharing_enabled") == "True" else False
        if field == "allowed_extensions":    
            new_allowed_extensions = request.form.getlist("extension_checkbox")
            for extension in get_all_extensions():
                if extension[0] in new_allowed_extensions and extension[1] == 0:
                    set_extension_status(extension[0], 1)
                elif not extension[0] in new_allowed_extensions and extension[1] == 1:
                    set_extension_status(extension[0], 0)
        if field == "add_extension":
            flash("This can't be changed on a demo instance!", "error")
        if field == "delete_extension":
            flash("This can't be changed on a demo instance!", "error")
        if field == "upload_folder":
            flash("This can't be changed on a demo instance!", "error")
    return render_template("panel/configuration.html", sharing_enabled = sharing_enabled, extensions = get_all_extensions(), upload_folder = get_config("upload_folder"))

@bp.route("/security", methods=["GET", "POST"])
@login_required
def security():
    if request.method == "POST":
        field = request.form.get("field")
        if field == "change_password":
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_new_password = request.form.get("confirm_new_password")
            if current_password and new_password and confirm_new_password:
                if check_password_hash(User.query.filter_by(username="admin").first().password, current_password):
                    if new_password == confirm_new_password:
                        flash("This can't be changed on a demo instance!", "error")
                    else:
                        flash("Passwords do not match!", "error")
                else:
                    flash("Password incorrect!", "error")
            else:
                flash("All fields are required!", "error")
        if field == "security_mode":
            flash("This can't be changed on a demo instance!", "error")
        if field == "add_ip":
            add_ip(request.form.get("ip"))
        if field == "delete_ip":
            delete_ip(request.form.get("ip"))
        if field == "edit_whitelist":
            flash("This can't be changed on a demo instance!", "error")
        if field == "edit_blacklist":
            flash("This can't be changed on a demo instance!", "error")
    return render_template("panel/security.html", security_mode=get_config("security_mode"), ips=get_all_ips())

# @bp.route("/docs")
# @login_required
# def docs():
#     readme_path = os.path.join(current_app.root_path, "..", "README.md")
#     with open(readme_path, 'r', encoding='utf-8') as readme:
#         readme_content = readme.read()
#     return render_template("panel/docs.html", readme_content = markdown.markdown(readme_content))

@bp.route("/logs")
@login_required
def logs():
    flash("You can't view logs in the demo mode!", "warning")
    logs_dir = os.path.join(current_app.root_path, "..", "logs")
    return render_template("/panel/logs.html", logs=os.listdir(logs_dir))

# @bp.route("/log/<file>")
# @login_required
# def logviewer(file):
#     log_file = os.path.join(current_app.root_path, "..", "logs", file)
#     with open(log_file, "r") as log:
#         content = log.read()
#     return Response(content, mimetype="text/plain")

@bp.route("/info")
@login_required
def info():
    host_ips=get_host_ips()
    port = get_port()
    
    qrs = list()
    
    for ip in host_ips:
        # if(ip == "127.0.0.1"):
        #     continue
        qr = qrcode.make(f"http://{ip}:{port}")
        buffer = BytesIO()  # ✅ Create an in-memory buffer
        qr.save(buffer, format="PNG")
        qrs.append((ip, base64.b64encode(buffer.getvalue()).decode("utf-8")))
    
    return render_template("panel/info.html", host_ips=host_ips, port=port, qrs = qrs)
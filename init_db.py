from app.models.config_value import ConfigValue
from app.models.file_extension import FileExtension
from app.models.ip import Ip
from app.models.user import User

from app import create_app
from app.extensions import db

import os
import secrets

app = create_app()

adminuser = User(username="admin", password="scrypt:32768:8:1$JRDPCndrkLCoOUtc$cf4578fe88d70b4e5f6bfe8b7fb7fda4d74cd5ae3b90104f8a415aed3bb1ef881d54dc8b3009210fa38e5a0dcfa4842d70f8c75ad9ab82d3454e4f6881cec9cd")
sharing_enabled = ConfigValue(name="sharing_enabled", value="True")
upload_folder = ConfigValue(name="upload_folder", value=os.path.join(app.root_path, "..", "uploads"))
security_mode = ConfigValue(name="security_mode", value="none")
demo = ConfigValue(name="demo", value="False")
ip = Ip(ip="127.0.0.1", on_whitelist=1, on_blacklist=0)

allowed_extensions = ["pdf", "txt", "zip", "csv", "gif", "jpg", "jpeg", "HEIC", "png", "svg", "pptx", "docx", "xlsx", "mp4", ]

if not os.path.exists(upload_folder.value):
    os.mkdir(upload_folder.value)

key_path = os.path.join(app.root_path, "..", "secret_key.txt")
if not os.path.exists(key_path):
    key = secrets.token_urlsafe(64)
    with open(key_path, "w") as f:
        f.write(key)
    print(key)

with app.app_context():
    db.create_all()
    
    db.session.add(adminuser)
    db.session.add(sharing_enabled)
    db.session.add(upload_folder)
    db.session.add(security_mode)
    db.session.add(demo)
    db.session.add(ip)
    
    for extension in allowed_extensions:
        db.session.add(FileExtension(name=extension, allowed=1))

    db.session.commit()
    
print("SUCCESS!")
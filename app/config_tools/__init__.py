from app.extensions import db

from app.models.config_value import ConfigValue
from app.models.file_extension import FileExtension
from app.models.ip import Ip

def get_config(name):
    return ConfigValue.query.filter_by(name=name).first().value

def set_config(name, value):
    current_config = ConfigValue.query.filter_by(name=name).first()
    current_config.value = value
    db.session.commit() 
    
def get_all_extensions():
    all_extensions = list()
    for extension in FileExtension.query.all():
        all_extensions.append((extension.name, extension.allowed))
    return all_extensions
    
def get_allowed_extensions():
    allowed_extensions = list()
    for extension in FileExtension.query.all():
        if(extension.allowed == 1):
            allowed_extensions.append(extension.name)
    return allowed_extensions

def allowed_file(filename):
    return "." in filename and filename.split(".")[-1] in get_allowed_extensions()

def set_extension_status(name, allowed):
    extension = FileExtension.query.filter_by(name=name).first()
    extension.allowed = allowed
    db.session.commit()
    
def add_extension(name):
    if FileExtension.query.filter_by(name=name).first() == None:
        db.session.add(FileExtension(name=name, allowed=1))
        db.session.commit()
    
def delete_extension(name):
    try:
        db.session.delete(FileExtension.query.filter_by(name=name).first())
        db.session.commit()
    except:
        pass
    
def add_ip(ip):
    if Ip.query.filter_by(ip=ip).first() == None:
        db.session.add(Ip(ip=ip, on_whitelist=0, on_blacklist=0))
        db.session.commit()
    
def delete_ip(ip):
    try:
        db.session.delete(Ip.query.filter_by(ip=ip).first())
        db.session.commit()
    except:
        pass

def get_all_ips():
    all_ips = list()
    for ip in Ip.query.all():
        all_ips.append((ip.ip, ip.on_whitelist, ip.on_blacklist))
    return all_ips

def set_whitelist_status(ip, status):
    current_ip = Ip.query.filter_by(ip=ip).first()
    current_ip.on_whitelist = status
    db.session.commit()
    
def set_blacklist_status(ip, status):
    current_ip = Ip.query.filter_by(ip=ip).first()
    current_ip.on_blacklist = status
    db.session.commit()
    
def get_whitelist_status(ip):
    current_ip = Ip.query.filter_by(ip=ip).first()
    if current_ip:
        return current_ip.on_whitelist
    return 0
    
def get_blacklist_status(ip):
    current_ip = Ip.query.filter_by(ip=ip).first()
    if current_ip:
        return current_ip.on_blacklist
    return 1
from app.extensions import db

class Ip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(24), nullable=False, unique=True)
    on_whitelist = db.Column(db.Integer, nullable=False)
    on_blacklist = db.Column(db.Integer, nullable=False)
from app.extensions import db

class FileExtension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    allowed = db.Column(db.Integer)
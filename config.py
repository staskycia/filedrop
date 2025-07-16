import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    with open(os.path.join(basedir, "secret_key.txt")) as f:
        SECRET_KEY = f.read()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
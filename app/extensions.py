from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from flask_login import LoginManager
from app.models.user import User

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message = "Please login to acces the panel!"
login_manager.login_message_category = "error"
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))
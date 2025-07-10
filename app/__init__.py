from flask import Flask

from config import Config
from configure_logging import configure_logging

from app.extensions import db, login_manager

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    configure_logging(app)
    
    #blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.panel import bp as panel_bp
    app.register_blueprint(panel_bp, url_prefix="/panel")

    return app
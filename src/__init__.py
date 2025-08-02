# application factory file
from flask import Flask
import os
from configs.config import Config
from .database.database import db
from flask_jwt_extended import JWTManager
from .auth.auth import auth_bp
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # load config
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    @app.route('/')
    def home():
        return {"meaage": "nowhwere like home"}
    

    db.app = app
    db.init_app(app)
    JWTManager(app)

    # registering blueprints
    app.register_blueprint(auth_bp)
    
    return app
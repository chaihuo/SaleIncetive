# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_logconfig import LogConfig
from flask_bootstrap import Bootstrap
from config import config

db = SQLAlchemy()
migrate = Migrate()
log_config = LogConfig()
login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    log_config.init_app(app)
    bootstrap.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app



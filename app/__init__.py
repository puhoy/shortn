__author__ = 'meatpuppet'


from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

from flask import Flask
from flask.ext.redis import FlaskRedis

import logging
from logging.handlers import RotatingFileHandler

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'

redis_store = FlaskRedis()


def create_app(config_name, log_level=logging.INFO):
    """
    this creates the app & initializes the logger (app.logger) as a rotated logmain

    :param config_name:
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    redis_store.init_app(app)

    handler = RotatingFileHandler('flask.log', maxBytes=10000, backupCount=1)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)

    #attach routes and custom error pages here

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
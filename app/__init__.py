from flask import Flask
from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.DevelopmentConfig')
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)
    return app

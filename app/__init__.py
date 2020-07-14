from flask import Flask
from flask_session import Session
# db.Model就是declarative_base
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

# from .models import *
from app import models


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.DevelopmentConfig')
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)
    Session(app)
    # 缺少数据库连接，把数据库连接配置传到sqlalchemy，
    db.init_app(app)  # init_app方法源码可以查看已有的配置
    return app

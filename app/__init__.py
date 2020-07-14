from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint
# import app.models
from app.models import *
def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.DevelopmentConfig')
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)
    # 实例化Session
    Session(app)
    # app里面有所有的配置，但是缺少数据库连接，把配置传到SQLAlchemy
    db.init_app(app)  # 可以查看init_app方法源码
    return app

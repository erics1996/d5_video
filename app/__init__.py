from flask import Flask, render_template
from flask_session import Session

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# from .models import *
from app import models


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.DevelopmentConfig')
    Session(app)
    # 缺少数据库连接，把数据库连接配置传到sqlalchemy，
    db.init_app(app)  # init_app方法源码可以查看已有的配置
    return app


"""
必须在app对象创建完成后才可以导入蓝图，否则在蓝图中使用app对象需要导入app对象时循环导入
"""
app = create_app()
from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

app.register_blueprint(admin_blueprint)
app.register_blueprint(home_blueprint)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

from app.home import home
from flask import render_template


@home.route("/login/", methods=['GET', 'POST'])
def login():
    return ''


@home.route("/logout/")
def logout():
    return ''


# 会员注册
@home.route("/register/", methods=['GET', 'POST'])
def register():
    return ''


# 修改会员资料
@home.route("/user/", methods=["GET", "POST"])
def user():
    return ''


# 修改密码
@home.route("/pwd/", methods=["GET", "POST"])
def pwd():
    return ''


# 评论列表
@home.route("/comments/<int:page>", methods=["GET"])
def per_comments_list(page=None):
    return ''


# 登陆日志
@home.route("/loginlog/<int:page>", methods=["GET"])
def loginlog(page=None):
    return ''

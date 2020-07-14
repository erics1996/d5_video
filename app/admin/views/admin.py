from .. import admin
from app import db, models
from flask import render_template


# 登录
@admin.route("/admin/login/", methods=["GET", "POST"])
def login():
    return ''


# 退出登录
@admin.route("/admin/logout/")
def logout():
    return ""


# 修改密码
@admin.route("/admin/pwd/", methods=["GET", "POST"])
def pwd():
    return ''


# 添加管理员
@admin.route("/admin/add/", methods=["GET", "POST"])
def admin_add():
    return ''


# 管理员列表
@admin.route("/admin/list/<int:page>", methods=["GET"])
def admin_list(page=None):
    return ''

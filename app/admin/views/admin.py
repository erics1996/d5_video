from .. import admin
from app import db, models
from flask import render_template
from ..forms.admin_form import AdminForm


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
    form = AdminForm()
    return render_template('admin/admin_add.html', form=form)


# 管理员列表
@admin.route("/admin/list/<int:page>", methods=["GET"])
def admin_list(page=None):
    return ''


# 管理员登录日志表
@admin.route("/admin/list/<int:page>", methods=["GET"])
def admin_loginlog_list(page):
    return ''

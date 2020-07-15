from .. import admin
from flask import render_template
from app import models


# 会员列表
@admin.route("/user/list/<int:page>", methods=["GET"])
def user_list(page=None):
    if not page:
        page = 1
    page_data = models.User.query.order_by(models.User.add_time.desc()).paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', page_data=page_data)


# 查看会员登录日志列表
@admin.route("/user/loginlog/list/<int:page>", methods=["GET"])
def user_loginlog_list(page):
    if not page:
        page = 1
    page_data = models.UserLog.query.order_by(models.UserLog.add_time.desc()).paginate(page=page, per_page=16)
    return render_template('admin/user_loginlog_list.html', page_data=page_data)


# 查看会员信息
@admin.route("/users/view/<int:id>", methods=["GET"])
def user_view(id):
    return ''

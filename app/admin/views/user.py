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
    page_data = models.UserLog.query.order_by(models.UserLog.add_time.desc()).paginate(page=page, per_page=10)
    # print(page_data.items)#[<UserLog 60>, <UserLog 59>, <UserLog 58>, <UserLog 57>, <UserLog 56>, <UserLog 55>, <UserLog 54>, <UserLog 53>, <UserLog 52>, <UserLog 51>]
    return render_template('admin/user_loginlog_list.html', page_data=page_data)


# 查看会员信息
@admin.route("/users/view/<int:id>", methods=["GET"])
def user_view(id):
    return ''

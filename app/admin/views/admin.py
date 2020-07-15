from .. import admin
from app import db, models
from flask import render_template, flash
from ..forms.admin_form import AdminForm
from werkzeug.security import generate_password_hash


# 添加管理员
@admin.route("/administrator/add/", methods=["GET", "POST"])
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin = models.Admin(
            name=data["name"],
            pwd=generate_password_hash("pwd"),
            role_id=data["role_id"],
            is_super=1  # 非超级管理员均为1
        )
        db.session.add(admin)
        db.session.commit()
        db.session.remove()
        flash("管理员添加成功！", "ok")
    return render_template('admin/admin_add.html', form=form)


# 管理员列表
@admin.route("/administrator/list/<int:page>", methods=["GET"])
def admin_list(page=None):
    if not page:
        page = 1
    page_data = models.Admin.query.paginate(page=page, per_page=10)
    return render_template('admin/admin_list.html', page_data=page_data)


@admin.route("/edit/", methods=["GET", "POST"])
def admin_edit():
    return ''


@admin.route("/del/", methods=["GET", "POST"])
def admin_del():
    return ''


# 登录
@admin.route("/login/", methods=["GET", "POST"])
def login():
    return ''


# 退出登录
@admin.route("/logout/")
def logout():
    return ""


# 修改密码
@admin.route("/pwd/", methods=["GET", "POST"])
def pwd():
    return ''


# 管理员登录日志表
@admin.route("/list/<int:page>", methods=["GET"])
def admin_loginlog_list(page):
    return ''

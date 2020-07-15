from .. import admin
from flask import render_template, flash, redirect, url_for
from ..forms.auth_form import AuthForm
from ...models import Auth
from app import db


# 权限添加
@admin.route("/admin/auth/add/", methods=["GET", "POST"])
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(name=data["name"], url=data["url"])
        db.session.add(auth)
        db.session.commit()
        db.session.remove()
        flash("权限添加成功！", "ok")
        return redirect(url_for('home.auth_add'))
    return render_template('admin/auth_add.html', form=form)


# 编辑权限
@admin.route("/admin/role/edit/<int:id>", methods=["GET", "POST"])
def auth_edit(id=None):
    return ''


# 权限列表
@admin.route("/admin/auth/list/<int:page>", methods=["GET"])
def auth_list(page=None):
    if not page:
        page = 1
    page_data = Auth.query.order_by(Auth.add_time.desc()).paginate(page=page, per_page=10)
    return render_template('admin/auth_list.html', page_data=page_data)


# 删除权限列表
@admin.route("/admin/auth/del/<int:id>", methods=["GET"])
def auth_del(id=None):
    return ''

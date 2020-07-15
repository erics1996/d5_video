from .. import admin
from ..forms.role_form import RoleForm
from flask import render_template, flash, redirect, url_for
from ...models import Role
from app import db


# 添加角色
@admin.route("/role/add/", methods=["GET", "POST"])
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        print(data['auth'])
        # auth=",".join(data["auth"])  # 用逗号分隔开，拼接成字符串
        role = Role(name=data["name"], auth=",".join(map(lambda v: str(v), data["auth"])))
        db.session.add(role)
        db.session.commit()
        db.session.remove()
        flash("角色添加成功！", "ok")
        return redirect(url_for('admin.role_add'))
    return render_template('admin/role_add.html', form=form)


# 角色列表
@admin.route("/role/list/<int:page>", methods=["GET"])
def role_list(page=None):
    if not page:
        page = 1
    page_data = Role.query.order_by(Role.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/role_list.html', page_data=page_data)


# 角色编辑
@admin.route("/role/list/<int:id>", methods=["GET"])
def role_edit(page=None):
    if not page:
        page = 1
    page_data = Role.query.order_by(Role.add_time.desc()).paginate(page=page, per_page=5)
    return render_template('admin/role_list.html', page_data=page_data)


# 角色删除
@admin.route("/role/del/<int:id>", methods=["GET"])
def role_del(id=None):
    return ''

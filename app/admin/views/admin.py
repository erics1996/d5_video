from .. import admin
from app import db, models
from flask import render_template, flash, request, redirect, url_for, session
from ..forms.admin_form import AdminForm
from ..forms.admin_form import AdminLoginForm
from werkzeug.security import generate_password_hash
from ...models import db
from .decorator import admin_login_decorator


# 添加管理员
@admin.route("/administrator/add/", methods=["GET", "POST"])
@admin_login_decorator
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        admin = models.Admin(
            name=data["name"],
            pwd=generate_password_hash(data["pwd"]),
            role_id=data["role_id"],
            is_super=1  # 非超级管理员均为1
        )
        db.session.add(admin)
        db.session.commit()
        db.session.remove()
        flash("管理员添加成功！", "ok")
    return render_template('admin/admin_add.html', form=form)


# 管理员列表
@admin.route("/administrator/list/<int:page>/", methods=["GET"])
@admin_login_decorator
def admin_list(page=None):
    page_data = models.Admin.query.paginate(page=page, per_page=10)
    return render_template('admin/admin_list.html', page_data=page_data)


@admin.route("/edit/", methods=["GET", "POST"])
@admin_login_decorator
def admin_edit():
    return ''


@admin.route("/del/<int:id>/", methods=["GET", "POST"])
@admin_login_decorator
def admin_del(id=None):
    admin = models.Admin.query.filter_by(id=id).first_or_404()
    db.session.delete(admin)
    db.session.commit()
    db.session.remove()
    return redirect(url_for('admin.admin_list', page=1))


# 登录
@admin.route("/login/", methods=["GET", "POST"])
def login():
    form = AdminLoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            # print(data["name"])
            # print(data["pwd"])
            admin = models.Admin.query.filter_by(name=data["name"]).first()
            # print(admin.check_pwd(data['pwd']))
            if not admin or \
                    not admin.check_pwd(data["pwd"]):
                flash("账号或密码错误！", "err")
                return redirect(url_for("admin.login", next=request.url))
            session["admin"] = admin.name
            session["admin_id"] = admin.id
            # session['face'] = admin.face
            admin_log = models.UserLog(
                admin_id=admin.id,
                ip=request.remote_addr
            )
            db.session.add(admin_log)
            db.session.commit()
            db.session.remove()
            return redirect(url_for("admin.index"))
    return render_template('admin/login.html', form=form)


# 退出登录
@admin.route("/logout/")
@admin_login_decorator
def logout():
    if session.get('admin') and session.get('admin_id'):
        session.pop('admin', None)
        session.pop('admin_id', None)
    return redirect(url_for('admin.login'))


# 修改密码
@admin.route("/pwd/", methods=["GET", "POST"])
@admin_login_decorator
def pwd():
    return ''


# 管理员登录日志表
@admin.route("/loginlog/list/<int:page>/", methods=["GET"])
@admin_login_decorator
def admin_loginlog_list(page=None):
    page_data = models.UserLog.query.join(
        models.Admin
    ).filter(
        models.UserLog.admin_id == models.Admin.id
    ).order_by(
        models.UserLog.add_time.desc()
    ).paginate(page=page, per_page=10)
    # print(page_data.items)#[<UserLog 60>, <UserLog 59>, <UserLog 58>, <UserLog 57>, <UserLog 56>, <UserLog 55>, <UserLog 54>, <UserLog 53>, <UserLog 52>, <UserLog 51>]
    return render_template('admin/admin_loginlog_list.html', page_data=page_data)

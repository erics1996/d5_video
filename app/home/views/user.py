from app.home import home
from flask import render_template, flash, request, redirect, url_for, session
from ..forms.user_form import RegisterForm, LoginForm
from ...models import User, UserLog
from app import db
from werkzeug.security import generate_password_hash
import uuid


# 会员注册
@home.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = User(
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                pwd=generate_password_hash(data["pwd"]),
                uuid=uuid.uuid4().hex
            )
            # print(user)  # <User (transient 140110428913776)>
            db.session.add(user)
            db.session.commit()
            db.session.remove()
            return redirect(url_for('home.login'))
            flash("注册成功，开始登录吧！", "ok")
    return render_template('home/register.html', form=form)


@home.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            data = form.data
            user = User.query.filter_by(name=data["name"]).first()
            if not user or not user.check_pwd(data["pwd"]):
                flash("账号或密码错误！", "err")
                return redirect(url_for("home.login"))
            session["user"] = user.name
            session["user_id"] = user.id
            user_log = UserLog(
                user_id=user.id,
                ip=request.remote_addr
            )
            db.session.add(user_log)
            db.session.commit()
            db.session.remove()
            return redirect(url_for("home.user"))
    return render_template('home/login.html', form=form)


@home.route("/logout/")
def logout():
    if session.get('user') and session.get('user_id'):
        session.pop('user', None)
        session.pop('user_id', None)
    return redirect(url_for('home.login'))


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

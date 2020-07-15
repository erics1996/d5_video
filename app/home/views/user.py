from app.home import home
from flask import render_template, flash, request, redirect, url_for, session
from ..forms.user_form import RegisterForm, LoginForm, UserDetailForm, PwdForm
from ...models import User, UserLog
from app import db
from werkzeug.security import generate_password_hash
import uuid
from functools import wraps


# 会员注册
@home.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form.data
            user = User(
                name=data["name"],
                nickname=data['name'],
                email=data["email"],
                phone=data["phone"],
                pwd=generate_password_hash(data["pwd"]),
                uuid=uuid.uuid4().hex,
                face='9825bc315c6034a86bd349b813468252092376b6.jpeg',
            )
            # print(users)  # <User (transient 140110428913776)>
            db.session.add(user)
            db.session.commit()
            db.session.remove()
            flash("注册成功，开始登录吧！", "ok")
            return redirect(url_for('home.login'))
    return render_template('home/register.html', form=form)


# 会员登录
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
            session['face'] = user.face
            user_log = UserLog(
                user_id=user.id,
                ip=request.remote_addr
            )
            db.session.add(user_log)
            db.session.commit()
            db.session.remove()
            return redirect(url_for("home.index"))
    return render_template('home/login.html', form=form)


@home.route("/logout/")
def logout():
    if session.get('user') and session.get('user_id'):
        session.pop('user', None)
        session.pop('user_id', None)
    return redirect(url_for('home.login'))


def user_login_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('home.login', next=request.url))
        return func(*args, **kwargs)

    return inner


# 修改会员基本资料
@home.route("/users/", methods=["GET", "POST"])
@user_login_decorator
def user():
    form = UserDetailForm()
    if request.method == "GET":
        user = User.query.get(int(session["user_id"]))
        # print(users)  # <User 1>
        form.name.data = user.name
        form.nickname.data = user.nickname
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info

    return render_template("home/user.html", form=form, user=user)


# 修改密码
@home.route("/pwd/", methods=["GET", "POST"])
def pwd():
    form = PwdForm()
    return render_template('home/pwd.html', form=form)


# 评论列表
@home.route("/comment/<int:page>", methods=["GET"])
def comment_list(page=None):
    return render_template('home/comment.html')


# 登陆日志
@home.route("/loginlog/<int:page>", methods=["GET"])
def loginlog(page=None):
    return render_template('home/loginlog.html')

from app.home import home
from flask import render_template, flash, request
from ..forms.user_form import RegisterForm
from ...models import User
from app import db
from werkzeug.security import generate_password_hash
import uuid


@home.route("/login/", methods=['GET', 'POST'])
def login():
    return ''


@home.route("/logout/")
def logout():
    return ''


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
            print(user)
            db.session.add(user)
            db.session.commit()
            db.session.remove()
            flash("注册成功！", "ok")
    return render_template('home/register.html', form=form)


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

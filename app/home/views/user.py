from app.home import home
from flask import render_template, flash, request, redirect, url_for, session, jsonify
from ..forms.user_form import RegisterForm, LoginForm, UserDetailForm, PwdForm
from ...models import User, UserLog, Comment, Movie
from app import db
from werkzeug.security import generate_password_hash
import uuid
from functools import wraps
from werkzeug.utils import secure_filename
import os
from ...utils.alter_filename import change_filename
from app import app


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
                face='default.jpeg',
            )
            # print(users)  # <User (transient 140110428913776)>
            db.session.add(user)
            db.session.commit()
            db.session.remove()
            flash("注册成功，开始登录吧！", "ok")
            return redirect(url_for('home.login', next=request.url))
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
                return redirect(url_for("home.login", next=request.url))
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


@home.route("/api/v1/user/logout/")
def logout():
    ret = {'status': 1, 'msg': None}
    try:
        if session.get('user') and session.get('user_id'):
            session.pop('user', None)
            session.pop('user_id', None)
    except Exception as e:
        ret['status'] = 0
        ret['msg'] = '退出失败！'
    return jsonify(ret)


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
    user = User.query.get(int(session["user_id"]))  # User.query.filter_by(id=session['user_id']).first()
    # print(users)  # <User 1>
    if request.method == "GET":
        form.name.data = user.name
        form.nickname.data = user.nickname
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        # 上传了头像会才会更新头像，没有上传不操作。图片支持中文名称
        if data['face']:
            if not os.path.exists(app.config["FACE_DIR"]):
                os.makedirs(app.config["FACE_DIR"])
            file_face = secure_filename(data['face'].filename)  # form.face.data <=> data['face']
            user.face = change_filename(file_face)  # 20200715164138eb5b145ddee1494a8c5d00dd1bb617c4.jpeg
            data['face'].save(app.config["FACE_DIR"] + user.face)
            if os.path.exists(app.config['FACE_DIR'] + session['face']):
                os.remove(app.config['FACE_DIR'] + session['face'])
        nickname_count = User.query.filter_by(nickname=data["nickname"]).count()
        if nickname_count == 1 and data["nickname"] != user.nickname:
            flash("昵称已存在！", "err")
            return redirect(url_for("home.user"))
        email_count = User.query.filter_by(email=data["email"]).count()
        if email_count == 1 and data["email"] != user.email:
            flash("邮箱已存在！", "err")
            return redirect(url_for("home.user"))
        phone_count = User.query.filter_by(phone=data["phone"]).count()
        if phone_count == 1 and data["phone"] != user.phone:
            flash("手机号码已存在！", "err")
            return redirect(url_for("home.user"))
        user.nickname = data["nickname"]
        user.email = data["email"]
        user.phone = data["phone"]
        user.info = data["info"]
        db.session.add(user)
        db.session.commit()
        db.session.remove()
        user = User.query.get(int(session["user_id"]))
        session['face'] = user.face
        flash("保存成功！", "ok")
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)


# 修改密码
@home.route("/pwd/", methods=["GET", "POST"])
@user_login_decorator
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        if data['old_pwd'] == data['new_pwd']:
            flash('新旧密码相同，系统不做修改！', 'err')
            return redirect(url_for('home.pwd'))
    return render_template('home/pwd.html', form=form)


# 评论列表
@home.route("/comment/", methods=["GET"])
@user_login_decorator
def comment_list():
    return render_template('home/comment.html')


# 登陆日志
@home.route("/loginlog/list/<int:page>/", methods=["GET"])
@user_login_decorator
def loginlog(page=None):
    # UserLog.query.filter_by(user_id=session.get('user_id'))：sql语句
    # UserLog.query.filter_by(user_id=session.get('user_id')).first()：<UserLog 1>
    # filter_by和order_by部分先后顺序
    page_data = UserLog.query.order_by(
        UserLog.add_time.desc()
    ).filter_by(
        user_id=session.get('user_id')
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)


@home.route('/comment/add/', methods=['POST'])
@user_login_decorator
def comment_add():
    ret = {'status': True, 'msg': None}
    try:
        # all = request.form  # ImmutableMultiDict([('comment_content', '你好'), ('user_id', '1'), ('movie_id', '3')])
        comment_content = request.form['comment_content']
        if len(comment_content) == 0:
            ret['status'] = False
            ret['msg'] = '评论内容不能为空！'
            return jsonify(ret)
        # print(comment_content, type(comment_content))  # 你好 <class 'str'>
        user_id = request.form['user_id']  # <class 'str'> 数据库是int，这里不使用int也可以
        movie_id = request.form['movie_id']  # <class 'str'>
        comment = Comment(
            content=comment_content,
            user_id=user_id,
            movie_id=movie_id
        )
        db.session.add(comment)
        db.session.commit()
        db.session.remove()
    except Exception as e:
        ret['status'] = False
        ret['msg'] = str(e)
        # ret['msg'] = '删除失败'
    return jsonify(ret)


@home.route('/movie/comment/list/', methods=['GET'])
def show_movie_comment(page=None):
    if not None:
        page = 1
    ret = {'status': True, 'msg': None}
    try:
        movie_id = request.args.get('movie_id')  # <class 'str'>
        movie_comment_obj_list_page_data = Comment.query.join(
            User
        ).join(
            Movie
        ).filter(
            Movie.id == Comment.movie_id,
            User.id == Comment.user_id,
            Movie.id == movie_id
        ).order_by(
            Comment.add_time.desc()
        ).paginate(page=page, per_page=8)
        # 加不加all()都可以
        ret['user'] = []
        for obj in movie_comment_obj_list_page_data.items:
            # print(obj.user.face)  # 202007162204485797a85fb89d4360a3e1fd63660105c8.jpg
            # print(obj.content)  # 太好看了！
            ret['user'].append({'username': obj.user.name, 'face': obj.user.face, 'movie_comment': obj.content,
                                'add_time': str(obj.add_time)})
            # ret['user']['face'].append(obj.user.face)
            # ret['user']['movie_comment'].append(obj.content)

    except Exception as e:
        print(e)  # Entity '<class 'app.models.User'>' has no property 'movie_id'
        ret['status'] = False
        ret['msg'] = str(e)  # Entity '<class 'app.models.User'>' has no property 'movie_id'
        ret['msg'] = '获取评论列表失败！'
    """
    import json
    print(json.dumps(ret))  # {"status": true, "msg": null, "user": {"face": "202007162204485797a85fb89d4360a3e1fd63660105c8.jpg", "comment_content": "\u592a\u597d\u770b\u4e86\uff01"}}
    print(jsonify(ret))  # <Response 151 bytes [200 OK]>
    """
    jsonify(ret)
    print(
        ret)  # {'status': True, 'msg': None, 'user': {'face': '202007162204485797a85fb89d4360a3e1fd63660105c8.jpg', 'comment_content': '太好看了！'}}
    return jsonify(ret)


# 获取用户评论列表
@home.route('/api/user/comment/list/')
def get_user_comment(page=None):
    if not page:
        page = 1
    ret = {'status': 1, 'msg': None}
    """
    # 如何查指定的字段
    comment = Comment.query.join(
        User
    ).join(
        Movie
    ).filter(
        Comment.user_id == User.id,
        Comment.movie_id == Movie.id
    ).order_by(
        Comment.add_time.desc()
    ).filter(Comment.content)
    SELECT comment.id AS comment_id, comment.content AS comment_content, comment.add_time AS comment_add_time, comment.movie_id AS comment_movie_id, comment.user_id AS comment_user_id 
FROM comment INNER JOIN user ON user.id = comment.user_id INNER JOIN movie ON movie.id = comment.movie_id 
WHERE comment.user_id = user.id AND comment.movie_id = movie.id AND comment.content ORDER BY comment.add_time DESC
    """
    comment_obj_list = Comment.query.join(
        Movie
    ).filter(
        Comment.movie_id == Movie.id
    ).order_by(
        Comment.add_time.desc()
    ).all()  # all()之后就成对象了
    ret['user'] = []
    for obj in comment_obj_list:
        ret['user'].append({'movie_name': obj.movie.title, 'add_time': obj.add_time, 'content': obj.content})
    print(ret)
    return jsonify(ret)

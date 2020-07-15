from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    nickname = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255))  # 头像
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符

    user_logs = db.relationship('UserLog', backref='user')  # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')  # 评论外键关系关联
    movie_cols = db.relationship('Moviecol', backref='user')  # 评论外键关系关联

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)  # 如果是True代表验证成功


class UserLog(db.Model):
    __tablename__ = "user_log"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    ip = db.Column(db.String(100))  # 登陆IP
    add_time = db.Column(db.DateTime, default=datetime.now)  # 登录时间

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户


class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 内容
    add_time = db.Column(db.DateTime, default=datetime.now)  # 评论时间

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户


class Moviecol(db.Model):
    __tablename__ = "movie_col"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    addtime = db.Column(db.DateTime, default=datetime.now)  # 评论时间

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户


class Movie(db.Model):
    __tablename__ = "movie"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 标号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    play_num = db.Column(db.BigInteger)  # 表放量
    comment_num = db.Column(db.BigInteger)  # 评论量
    area = db.Column(db.String(255))  # 地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    add_time = db.Column(db.DateTime, default=datetime.now)

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    comments = db.relationship("Comment", backref='movie')  # 电影外键关系关联
    movie_cols = db.relationship("Moviecol", backref='movie')  # 电影外键关系关联


class Tag(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    add_time = db.Column(db.DateTime, default=datetime.now)  # 添加时间

    movies = db.relationship("Movie", backref='tag')  # 电影外键关系关联


class Preview(db.Model):
    __tablename__ = "preview"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    add_time = db.Column(db.DateTime, default=datetime.now)  # 上映时间


class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 角色名称
    auth = db.Column(db.String(600))  # 权限列表
    add_time = db.Column(db.DateTime, default=datetime.now)  # 角色添加时间
    admins = db.relationship('Admin', backref='role')


class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员，0为超级管理员

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色

    admin_logs = db.relationship("AdminLog", backref='admin')  # 外键关系关联
    op_logs = db.relationship("OpLog", backref='admin')  # 外键关系关联


class AdminLog(db.Model):
    __tablename__ = "admin_log"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    ip = db.Column(db.String(100))  # 登陆IP
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员


class OpLog(db.Model):
    __tablename__ = "op_log"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    ip = db.Column(db.String(100))  # 登陆IP
    reason = db.Column(db.String(600))  # 操作原因
    add_time = db.Column(db.DateTime, default=datetime.now)  # 登录时间
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员


class Auth(db.Model):
    __tablename__ = "auth"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号add
    name = db.Column(db.String(100), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 权限名称
    add_time = db.Column(db.DateTime, default=datetime.now)  # 添加时间

from app import db
from datetime import datetime


# db.Model=make_declarative_base
class Auth(db.Model):
    __tablename__ = "auth"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 权限名称
    addtime = db.Column(db.DateTime, default=datetime.now)  # 添加时间

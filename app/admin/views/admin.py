from .. import admin
from app import db,models

@admin.route('/admin/')
def index():
    """
    添加数据，如果没有连接db.session(create_scoped_session)内部会自动创建连接
    """
    db.session.add(models.Auth(name='',url=''))
    db.session.commit()
    # 释放连接
    db.session.remove()
    """
    查询数据
    """
    ret = db.session.query(models.Auth).all()
    print(ret)
    db.session.remove()
    return 'index'

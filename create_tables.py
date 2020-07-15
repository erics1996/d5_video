from app import db
from app import app  # from manage import app

app_ctx = app.app_context()  # AppContext对象里面有app和g
"""
1.去指定的请求上下文中找app,再去app中找配置文件和Models
2.在执行db.create_all()之前，必须先把app和g封装成AppContext对象，然后放到Local中，才就可以取到
3.没有用到应用上下文request/session。app上下文中有app和g，g没有用上，但app用上了！
4.为什么要把上下文管理分为应用上下文request/session和请求上下文app/g?
① Flask的SQLALchemy生成表结构时候用不上应用上下文request/session。
② 如果用到request/session需要传请求，并非http操作，生成表结构只是个离线脚本)
"""
"""
__enter__：LocalStack().push()，通过LocalStack把AppContext的对象(app_ctx)放到Local中
"""
with app_ctx:
    db.create_all()  # 内部会从app_ctx中获取app，再从app中获取配置文件
"""
__exit__：LocalStack().pop(),通过LocalStack再从Local中移出
"""

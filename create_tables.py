from app import db, create_app

# 和from manage import app一样
app = create_app()
app_ctx = app.app_context()  # AppContext对象里面有app和g
"""
__enter__：通过LocalStack把AppContext对象app_ctx放到Local中
"""
with app_ctx:
    """
    去指定的请求上下文中找app,再去app中找配置文件和Models，帮助我们生成表。在执行db.create_all()之前，必须先把app和g封装成AppContext对象，然后放到
    Local中，再create_all()的时候就可以取到！没有用到request上下文和session。app上下文中有app和g，g没有用上，但app用上了！(
    为什么要分为应用上下文request/session和请求上下文app/g?Flask的SQLALchemy生成表结构时候用不上session和request，没有意义所以要分开。况且如果有request/session
    需要传请求，这不是请求，并非http操作，是一个脚本)
    """
    db.create_all()  # 内部会调用LocalStack去Local中获取app，再去app中获取配置文件
"""
__exit__：通过Local，在LocalStack中把app移除
"""

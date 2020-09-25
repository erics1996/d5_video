from functools import wraps
from flask import session, redirect, url_for, request


# 装饰器
def user_login_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for('home.login', next=request.url))
        return func(*args, **kwargs)

    return inner

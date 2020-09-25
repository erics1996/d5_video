from functools import wraps
from flask import session, redirect, url_for, request


def admin_login_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin.login', next=request.url))
        return func(*args, **kwargs)

    return inner

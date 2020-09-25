from .. import admin
from flask import render_template
from .decorator import admin_login_decorator


@admin.route('/')
@admin_login_decorator
def index():
    return render_template('admin/index.html')

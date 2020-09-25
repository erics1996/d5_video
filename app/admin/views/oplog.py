from .. import admin
from flask import render_template
from .decorator import admin_login_decorator

@admin.route('/admin/')
def oplog_list():
    return ''

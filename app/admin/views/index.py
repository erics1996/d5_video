from .. import admin
from flask import render_template


@admin.route('/index/')
def index():
    return render_template('admin/index.html')

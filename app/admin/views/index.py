from .. import admin
from flask import render_template


@admin.route('/v1/admin/')
def index():
    return render_template('admin/index.html')

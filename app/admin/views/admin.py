from .. import admin
from app import db


@admin.route('/admin/')
def index():
    return 'index'

from .. import admin


@admin.route('/admin/')
def index():
    return 'index'
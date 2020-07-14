from flask import Blueprint

admin = Blueprint('admin', __name__)
import app.admin.views.admin
import app.admin.views.index
import app.admin.views.tag
import app.admin.views.movie
import app.admin.views.preview
import app.admin.views.user

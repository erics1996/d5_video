from flask import Blueprint

admin = Blueprint('admin', __name__)
# from app.admin.views.admin import index
import app.admin.views.admin
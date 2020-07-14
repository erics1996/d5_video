from flask import Blueprint

home = Blueprint('home', __name__)

import app.home.views.user
import app.home.views.movie
import app.home.views.index
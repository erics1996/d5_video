from app.home import home
from flask import render_template


@home.route('/')
def index():
    return ''
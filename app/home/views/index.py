from app.home import home
from flask import render_template


@home.route('/index.html')
def index():
    return render_template('home/index.html')
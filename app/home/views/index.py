from app.home import home
from flask import render_template


@home.route('/')
def index():
    return render_template('home/index.html')

@home.route('/index.html')
def index2():
    return render_template('home/index.html')
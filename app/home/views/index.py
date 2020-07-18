from app.home import home
from flask import render_template


@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/index.html')
def index2():
    return render_template('home/index.html')


@home.route('/aboutwebsite.html')
def about_website():
    return render_template('home/aboutwebsite.html')


@home.route('/disclaimer.html')
def disclaimer():
    return render_template('home/disclaimer.html')


@home.route('/contact.html')
def contact():
    return render_template('home/contact.html')


@home.route('/blueprint.html')
def blueprint():
    return render_template('home/blueprint.html')

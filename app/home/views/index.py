from app.home import home
from flask import render_template
from ...models import Preview


@home.route('/')
def index():
    preview_data = Preview.query.all()
    # print(preview_data)  # [<Preview 17>]
    first_preview_id = Preview.query.order_by(Preview.id.asc()).first().id  # <Preview 17>
    # first_preview_id = Preview.query.order_by(Preview.id.asc())  # sql
    # print(first_preview_id.id)
    return render_template('home/index.html', preview_data=preview_data, first_preview_id=first_preview_id)


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

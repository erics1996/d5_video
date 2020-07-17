from .. import admin
from flask import render_template, flash, url_for, redirect
from ..forms.movie_form import MovieForm
from ...models import db
from werkzeug.utils import secure_filename
import os
from ...utils.alter_filename import change_filename
from app import app
from ...models import Movie, Tag


# 添加电影
@admin.route("/movie/add/", methods=["GET", "POST"])
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        # file_url = secure_filename(form.url.data.filename)
        file_url = secure_filename(data['url'].filename)
        file_logo = secure_filename(data['logo'].filename)
        # 创建电影资源存放目录
        if not os.path.exists(app.config["MOVIE_DIR"]):
            os.makedirs(app.config["MOVIE_DIR"])
        # 创建电影资源封面存放目录
        if not os.path.exists(app.config["MOVIE_LOGO_DIR"]):
            os.makedirs(app.config["MOVIE_LOGO_DIR"])
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["MOVIE_DIR"] + url)
        form.logo.data.save(app.config["MOVIE_LOGO_DIR"] + logo)
        movie = Movie(
            title=data["title"],
            url=url,
            info=data["info"],
            logo=logo,
            star=int(data["star"]),
            play_num=0,
            comment_num=0,
            tag_id=int(data["tag_id"]),
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"]
        )
        db.session.add(movie)
        db.session.commit()
        db.session.remove()
        flash("添加电影成功！", "ok")
        return redirect(url_for('admin.movie_add'))
    return render_template("admin/movie_add.html", form=form)


# 电影列表
@admin.route("/movie/list/")
def movie_list(page=None):
    if not page:
        page = 1
    # page_data = Movie.query.order_by(Movie.add_time.desc()).paginate(page=page, per_page=10)
    page_data = Movie.query.join(Tag).filter(
        Movie.tag_id == Tag.id
    ).order_by(Movie.add_time.desc()).paginate(page=page, per_page=10)
    # print(page_data.items)
    return render_template("admin/movie_list.html", page_data=page_data)

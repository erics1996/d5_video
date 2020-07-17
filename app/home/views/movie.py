from app.home import home
from flask import render_template, request
from ... import models
from app import db


@home.route("/search/<int:page>/")
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    movie_count = models.Movie.query.filter(
        models.Movie.title.ilike('%' + key + '%')
    ).count()
    page_data = models.Movie.query.filter(
        models.Movie.title.ilike('%' + key + '%')
    ).order_by(
        models.Movie.add_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/search.html", page=page, key=key, page_data=page_data, movie_count=movie_count)


@home.route("/play/<int:id>/", methods=["GET", "POST"])
def play(id=None):
    movie = models.Movie.query.filter_by(id=id).first_or_404()
    movie.play_num += 1
    db.session.add(movie)
    db.session.commit()
    db.session.remove()
    movie = models.Movie.query.filter_by(id=id).first_or_404()
    return render_template('home/movie_play.html', movie=movie)

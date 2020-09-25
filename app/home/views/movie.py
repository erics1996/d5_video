from app.home import home
from flask import render_template, request, jsonify
from ... import models
from app import db
from .user import user_login_decorator


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


@home.route("/play/<int:id>.html", methods=["GET", "POST"])
def play(id=None):
    movie = models.Movie.query.filter_by(id=id).first_or_404()
    movie.play_num += 1
    db.session.add(movie)
    db.session.commit()
    db.session.remove()
    movie = models.Movie.query.filter_by(id=id).first_or_404()
    return render_template('home/movie_play.html', movie=movie)


# 接口：电影列表
@home.route('/api/movie/list/', methods=['GET'])
def get_movie_list():
    ret = {'code': 1, 'msg': None}
    try:
        # movie_list = models.Movie.query#sql
        movie_list = models.Movie.query.all()
        # print(movie_list)  # [<Movie 2>, <Movie 3>]
        ret['movies'] = []
        for movie_obj in movie_list:
            ret['movies'].append(
                {'id': movie_obj.id, 'info': movie_obj.info, 'logo': movie_obj.logo, 'title': movie_obj.title})
        # print(ret)  # {'code': 1, 'msg': None, 'movies': [{'id': 2, 'info': '本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”，讲述了两个女主人公莉拉和埃莱娜的一生。本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”', 'logo': '20200716202150e030901ca71f45a7aa1fbf547e154e0b.jpeg'}, {'id': 3, 'info': '本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”，讲述了两个女主人公莉拉和埃莱娜的一生。本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”', 'logo': '20200716203111400d0e5b8ff544d4b277f692e9bea4b1.jpeg'}]}
        # jsonify(ret)
        # print(ret)  # {'code': 1, 'msg': None, 'movies': [{'id': 2, 'info': '本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”，讲述了两个女主人公莉拉和埃莱娜的一生。本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”', 'logo': '20200716202150e030901ca71f45a7aa1fbf547e154e0b.jpeg'}, {'id': 3, 'info': '本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”，讲述了两个女主人公莉拉和埃莱娜的一生。本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”', 'logo': '20200716203111400d0e5b8ff544d4b277f692e9bea4b1.jpeg'}]}
    except Exception as e:
        ret['code'] = 0
        ret['msg'] = '获取电影列表失败！'
        print(e)
    return jsonify(ret)


# 添加电影收藏
@home.route("/moviecol/add/", methods=["GET", 'POST'])
def moviecol_add():
    user_id = request.args.get("user_id", "")
    movie_id = request.args.get("movie_id", "")
    moviecol = models.Moviecol.query.filter_by(
        user_id=user_id,
        movie_id=movie_id
    ).count()
    data = dict()
    if moviecol == 1:
        data = dict(ok=1)  # {'ok': 1}表示已经收藏

    if moviecol == 0:
        moviecol = models.Moviecol(
            user_id=user_id,
            movie_id=movie_id
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=0)  # {'ok': 0}表示需要收藏
    return jsonify(data)


# 电影收藏状态
@home.route('/api/moviecol/status/')
def get_moviecol_status():
    user_id = request.args.get("user_id", "")
    movie_id = request.args.get("movie_id", "")
    moviecol = models.Moviecol.query.filter_by(
        user_id=user_id,
        movie_id=movie_id
    ).count()
    if moviecol == 1:
        data = dict(ok=1)  # {'ok': 1}表示已经收藏
    else:
        data = dict(ok=0)
    return jsonify(data)

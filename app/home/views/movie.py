from app.home import home
from flask import render_template, request, jsonify
from ... import models
from ...models import Comment, User, Movie
from app import db
from .user import user_login_decorator


# 搜索电影
@home.route("/movie/search/<int:page>/")
def movie_search(page=None):
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
    return render_template("home/movie_search.html", page=page, key=key, page_data=page_data, movie_count=movie_count)


# 电影播放
@home.route("/movie/play/<int:id>.html", methods=["GET", "POST"])
def movie_play(id=None):
    movie = models.Movie.query.filter_by(id=id).first_or_404()

    movie.play_num += 1
    db.session.add(movie)
    db.session.commit()
    db.session.remove()
    movie = models.Movie.query.filter_by(id=id).first_or_404()
    comment_count = models.Comment.query.join(
        models.Movie
    ).filter(
        models.Comment.movie_id == models.Movie.id,
        models.Movie.id == id
    ).count()
    # print(comment_count)
    return render_template('home/movie_play.html', movie=movie, comment_count=comment_count)


# 接口：电影列表
# @home.route('/api/movie/list/', methods=['GET'])
# def get_movie_list():
#     ret = {'code': 1, 'msg': None}
#     try:
#         # movie_list = models.Movie.query#sql
#         movie_list = models.Movie.query.all()
#         # print(movie_list)  # [<Movie 2>, <Movie 3>]
#         ret['movies'] = []
#         for movie_obj in movie_list:
#             ret['movies'].append(
#                 {'id': movie_obj.id, 'info': movie_obj.info, 'logo': movie_obj.logo, 'title': movie_obj.title})
#         # print(ret)  # {'code': 1, 'msg': None, 'movies': [{'id': 2, 'info': '本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”，讲述了两个女主人公莉拉和埃莱娜的一生。本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”', 'logo': '20200716202150e030901ca71f45a7aa1fbf547e154e0b.jpeg'}, {'id': 3, 'info': '本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”，讲述了两个女主人公莉拉和埃莱娜的一生。本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”', 'logo': '20200716203111400d0e5b8ff544d4b277f692e9bea4b1.jpeg'}]}
#         # jsonify(ret)
#         # print(ret)  # {'code': 1, 'msg': None, 'movies': [{'id': 2, 'info': '本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”，讲述了两个女主人公莉拉和埃莱娜的一生。本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”', 'logo': '20200716202150e030901ca71f45a7aa1fbf547e154e0b.jpeg'}, {'id': 3, 'info': '本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”，讲述了两个女主人公莉拉和埃莱娜的一生。本剧改编自小说家埃莱娜·费兰特的“那不勒斯四部曲”', 'logo': '20200716203111400d0e5b8ff544d4b277f692e9bea4b1.jpeg'}]}
#     except Exception as e:
#         ret['code'] = 0
#         ret['msg'] = '获取电影列表失败！'
#         print(e)
#     return jsonify(ret)

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
        data = dict(ok=0)

    if moviecol == 0:
        moviecol = models.Moviecol(
            user_id=user_id,
            movie_id=movie_id
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)
    return jsonify(data)


@home.route("/moviecol/del/", methods=["GET", 'POST'])
def moviecol_cancel():
    user_id = request.args.get("user_id", "")
    movie_id = request.args.get("movie_id", "")
    moviecol = models.Moviecol.query.filter_by(user_id=user_id, movie_id=movie_id).first_or_404()
    # print(moviecol)
    data = dict(ok=0)  # {'ok': 0}表示取消失败
    if moviecol:
        db.session.delete(moviecol)
        db.session.commit()
        db.session.remove()
        data = dict(ok=1)  # {'ok': 1}表示取消成功
    return jsonify(data)


# 电影收藏状态(接口)
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


# 添加评论(接口)
@home.route('/movie/comment/add/', methods=['POST'])
@user_login_decorator
def comment_add():
    ret = {'status': True, 'msg': None}
    try:
        # all = request.form  # ImmutableMultiDict([('comment_content', '你好'), ('user_id', '1'), ('movie_id', '3')])
        comment_content = request.form['comment_content']
        if len(comment_content) == 0:
            ret['status'] = False
            ret['msg'] = '评论内容不能为空！'
            return jsonify(ret)
        # print(comment_content, type(comment_content))  # 你好 <class 'str'>
        user_id = request.form['user_id']  # <class 'str'> 数据库是int，这里不使用int也可以
        movie_id = request.form['movie_id']  # <class 'str'>
        comment = Comment(
            content=comment_content,
            user_id=user_id,
            movie_id=movie_id
        )
        db.session.add(comment)
        db.session.commit()
        db.session.remove()
    except Exception as e:
        ret['status'] = False
        ret['msg'] = str(e)
        # ret['msg'] = '删除失败'
    return jsonify(ret)


# 评论列表(接口)
@home.route('/movie/comment/list/', methods=['GET'])
def show_movie_comment(page=None):
    if not None:
        page = 1
    ret = {'status': True, 'msg': None}
    try:
        movie_id = request.args.get('movie_id')  # <class 'str'>
        movie_comment_obj_list_page_data = Comment.query.join(
            User
        ).join(
            Movie
        ).filter(
            Movie.id == Comment.movie_id,
            User.id == Comment.user_id,
            Movie.id == movie_id
        ).order_by(
            Comment.add_time.desc()
        ).paginate(page=page, per_page=8)
        # 加不加all()都可以
        ret['user'] = []
        for obj in movie_comment_obj_list_page_data.items:
            # print(obj.user.face)  # 202007162204485797a85fb89d4360a3e1fd63660105c8.jpg
            # print(obj.content)  # 太好看了！
            ret['user'].append({'username': obj.user.name, 'face': obj.user.face, 'movie_comment': obj.content,
                                'add_time': str(obj.add_time)})
            # ret['user']['face'].append(obj.user.face)
            # ret['user']['movie_comment'].append(obj.content)

    except Exception as e:
        print(e)  # Entity '<class 'app.models.User'>' has no property 'movie_id'
        ret['status'] = False
        ret['msg'] = str(e)  # Entity '<class 'app.models.User'>' has no property 'movie_id'
        ret['msg'] = '获取评论列表失败！'
    """
    import json
    print(json.dumps(ret))  # {"status": true, "msg": null, "user": {"face": "202007162204485797a85fb89d4360a3e1fd63660105c8.jpg", "comment_content": "\u592a\u597d\u770b\u4e86\uff01"}}
    print(jsonify(ret))  # <Response 151 bytes [200 OK]>
    """
    jsonify(ret)
    print(
        ret)  # {'status': True, 'msg': None, 'user': {'face': '202007162204485797a85fb89d4360a3e1fd63660105c8.jpg', 'comment_content': '太好看了！'}}
    return jsonify(ret)

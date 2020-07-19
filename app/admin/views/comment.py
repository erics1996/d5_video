from .. import admin
from flask import render_template, redirect, url_for
from ...models import Comment, User, Movie
from ...models import db


# 评论列表
@admin.route("/comment/list/<int:page>/", methods=["GET"])
def comment_list(page=None):
    page_data = Comment.query.join(
        User
    ).join(
        Movie
    ).filter(
        User.id == Comment.user_id,
        Movie.id == Comment.movie_id
    ).order_by(
        Comment.add_time.desc()
    ).paginate(page=page, per_page=20)

    return render_template('admin/comment_list.html', page_data=page_data)


# 删除评论
@admin.route("/comment/del/<int:id>/", methods=["GET"])
def comment_del(id=None):
    comment = Comment.query.filter_by(id=id).first_or_404()  # <Comment 45>
    """
    comment = Comment.query.filter_by(id=id)
    SELECT comment.id AS comment_id, comment.content AS comment_content, comment.add_time AS comment_add_time, comment.movie_id AS comment_movie_id, comment.user_id AS comment_user_id 
    FROM comment 
    WHERE comment.id = %(id_1)s
    """
    db.session.delete(comment)
    db.session.commit()
    db.session.remove()
    return redirect(url_for('admin.comment_list', page=1))

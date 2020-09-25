from .. import admin
from .decorator import admin_login_decorator
from ... import models
from flask import render_template, redirect, url_for
from ...models import db


# 收藏列表
@admin.route("/moviecol/list/<int:page>")
@admin_login_decorator
def moviecol_list(page=None):
    page_data = models.Moviecol.query.order_by(models.Moviecol.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/moviecol_list.html', page_data=page_data)


# 删除电影收藏列表
@admin.route("/moviecol/del/<int:id>/", methods=["GET"])
@admin_login_decorator
def moviecol_del(id=None):
    moviecol = models.Moviecol.query.filter_by(id=id).first()
    db.session.delete(moviecol)
    db.session.commit()
    db.session.remove()
    return redirect(url_for('admin.moviecol_list', page=1))

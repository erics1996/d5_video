from .. import admin
from flask import render_template, flash, redirect, url_for
from ..forms.tag_form import TagForm
from ...models import Tag
from app import db


# 添加标签
@admin.route("/tag/add/", methods=["GET", "POST"])
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag_count == 1:
            flash('标签已存在！', 'err')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(name=data['name'])
        db.session.add(tag)
        db.session.commit()
        db.session.remove()
        flash('标签添加成功！', 'ok')
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


# 标签列表
@admin.route("/tag/list/<int:page>", methods=["GET"])
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.add_time.desc()
    ).paginate(page=page, per_page=20)
    return render_template('admin/tag_list.html', page_data=page_data)


# 编辑标签
@admin.route("/tag/edit/<int:id>", methods=["GET", "POST"])
def tag_edit(id=None):
    return ''


# 删除标签
@admin.route("/tag/del/<int:id>", methods=["GET"])
def tag_del(id=None):
    return ''

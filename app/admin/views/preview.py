from .. import admin
from ..forms.preview_form import PreviewForm
from flask import render_template, redirect, url_for, flash
from ...models import Preview
from werkzeug.utils import secure_filename
from app.utils.alter_filename import change_filename
from ...models import db
from app import app
import os


# 添加电影预告
@admin.route("/preview/add/", methods=["POST", "GET"])
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        try:
            if not os.path.exists(app.config['PREVIEW_DIR']):
                os.mkdir(app.config['PREVIEW_DIR'])
            cover_picture = secure_filename(data['cover_picture'].filename)  # 不支持中文名的图片
            new_cover_picture = secure_filename(change_filename(cover_picture))
            data['cover_picture'].save(app.config['PREVIEW_DIR'] + new_cover_picture)
            preview = Preview(
                title=data['title'],
                cover_picture=new_cover_picture
            )
            db.session.add(preview)
            db.session.commit()
            db.session.remove()
            flash(message='添加成功！', category='ok')
        except Exception as e:
            print(e.args)
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)


# 电影预告列表
@admin.route("/preview/list/")
def preview_list(page=None):
    page_data = Preview.query.paginate(page=1, per_page=10)
    return render_template('admin/preview_list.html', page_data=page_data)


@admin.route('/preview/edit/')
def preview_edit(page=None):
    return ''


@admin.route('/preview/del/<int:id>/')
def preview_del(id):
    preview = Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    db.session.remove()
    flash('删除成功！', category='ok')
    return redirect(url_for('admin.preview_list'))

from .. import admin


# 添加电影
@admin.route("/admin/d5video/add/", methods=["GET", "POST"])
def movie_add():
    return ''


# 电影列表
@admin.route("/admin/d5video/list/")
def movie_list():
    return ''


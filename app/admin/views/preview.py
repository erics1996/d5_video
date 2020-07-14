from .. import admin


# 添加电影预告
@admin.route("/admin/preview/add/", methods=["POST", "GET"])
def preview_add():
    return ''


# 电影预告列表
@admin.route("/admin/preview/list/")
def preview_list():
    return ''

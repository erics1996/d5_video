from .. import admin


# 收藏列表
@admin.route("/admin/moviecol/list/<int:page>")
def moviecol_list(page=None):
    return ''


# 删除电影收藏列表
@admin.route("/admin/moviecol/del/<int:id>", methods=["GET"])
def moviecol_del(id=None):
    return ''

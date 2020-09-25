from .. import admin
from .decorator import admin_login_decorator

# 收藏列表
@admin.route("/admin/moviecol/list/<int:page>")
@admin_login_decorator
def moviecol_list(page=None):
    return ''


# 删除电影收藏列表
@admin.route("/admin/moviecol/del/<int:id>", methods=["GET"])
@admin_login_decorator
def moviecol_del(id=None):
    return ''

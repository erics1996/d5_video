from .. import admin


# 添加角色
@admin.route("/admin/role/add/", methods=["GET", "POST"])
def role_add():
    return ''


# 角色列表
@admin.route("/admin/role/list/<int:page>", methods=["GET"])
def role_list(page=None):
    return ''


# 角色删除
@admin.route("/admin/role/del/<int:id>", methods=["GET"])
def role_del(id=None):
    return ''
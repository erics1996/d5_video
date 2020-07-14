from .. import admin


# 权限添加
@admin.route("/admin/auth/add/", methods=["GET", "POST"])
def auth_add():
    return ''


# 编辑权限
@admin.route("/admin/role/edit/<int:id>", methods=["GET", "POST"])
def role_edit(id=None):
    return ''


# 权限列表
@admin.route("/admin/auth/list/<int:page>", methods=["GET"])
def auth_list(page=None):
    return ''


# 删除权限列表
@admin.route("/admin/auth/del/<int:id>", methods=["GET"])
def auth_del(id=None):
    return ''

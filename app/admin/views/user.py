from .. import admin


# 用户列表
@admin.route("/admin/users/list/<int:page>", methods=["GET"])
def user_list(page=None):
    return ''


# 查看会员信息
@admin.route("/admin/users/view/<int:id>", methods=["GET"])
def user_view():
    return ''

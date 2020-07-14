from .. import admin


# 添加标签
@admin.route("/admin/tag/add/", methods=["GET", "POST"])
def tag_add():
    return ''


# 标签列表
@admin.route("/admin/tag/list/<int:page>", methods=["GET"])
def tag_list(page=None):
    return ''


# 删除标签
@admin.route("/admin/tag/del/<int:id>", methods=["GET"])
def tag_del(id=None):
    return ''


# 编辑标签
@admin.route("/admin/tag/edit/<int:id>", methods=["GET", "POST"])
def tag_edit(id=None):
    return ''

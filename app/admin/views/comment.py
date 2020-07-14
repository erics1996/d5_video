from .. import admin


# 评论列表
@admin.route("/admin/comment/list/<int:page>", methods=["GET"])
def comment_list(page=None):
    return ''


# 删除评论
@admin.route("/admin/comment/del/<int:id>", methods=["GET"])
def comment_del(id=None):
    return ''

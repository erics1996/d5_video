from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired
from ...models import Auth

auth_list = Auth.query.all()


class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称！")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入角色名称！",
        }
    )
    auth = SelectMultipleField(
        label="操作权限",
        validators=[
            DataRequired("请选择操作权限！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in auth_list],
        description="操作权限",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )

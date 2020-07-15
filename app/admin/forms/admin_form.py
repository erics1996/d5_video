from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class AdminForm(FlaskForm):
    name = StringField(
        label="管理员账号",
        validators=[
            DataRequired("请输入管理员账号！")
        ],
        description="管理员账号",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入管理员账号！",
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("请输入管理员密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码！",
        }

    )
    repwd = PasswordField(
        label="重复管理员密码",
        validators=[
            DataRequired("请重复管理员密码！"),
            EqualTo('pwd', message="两次密码不一致")
        ],
        description="重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请重复管理员密码！",
        }
    )
    role_id = SelectField(
        label="所属角色",
        coerce=int,
        # choices=[(v.id, v.name) for v in role_list],  # 生成角色列表，列表有角色id和名字
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

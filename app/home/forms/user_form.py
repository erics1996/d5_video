from flask_wtf import FlaskForm  # FlaskForm是表单的基类
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from ...models import User


class RegisterForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control input",
            "placeholder": "请输入账号！",
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired("请输入邮箱！"),
            Email("邮箱格式不正确！")
        ],
        description="昵称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱！",
        }
    )
    phone = StringField(
        label='手机号',
        validators=[
            DataRequired("请输入手机号！"),
            Regexp('1[345789]\\d{9}', message='手机号格式不正确！')
        ],
        description="手机号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机号！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！"
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('pwd', message='两次密码不一致')
        ],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入确认密码！",
        }
    )

    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-log btn-primary btn-block"
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user >= 1:
            raise ValidationError('账号已经存在！')

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user >= 1:
            raise ValidationError('该手机号已被注册！')

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user >= 1:
            raise ValidationError('该邮箱已被注册！')

from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError
from ...models import Preview


class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题！")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题！"
        }
    )
    cover_picture = FileField(
        validators=[
            DataRequired("请上传预告封面！")
        ],
        description="预告封面",
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    def validate_title(self, field):
        title = field.data
        preview = Preview.query.filter_by(
            title=title
        ).first()
        if preview:
            raise ValidationError("预告标题已经存在！")

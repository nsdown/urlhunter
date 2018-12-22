from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from urlhunter.models import User


class Unique(object):
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        self.message = message if message else '已被占用'

    def __call__(self, form, field):
        check = self.model.query.filter(self.field==field.data).first()
        if check:
            raise ValidationError(self.message)


class LoginForm(FlaskForm):
    username = StringField('用户名', [DataRequired()])
    password = PasswordField('密码', [DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', [DataRequired(), Unique(User, User.username, '该用户名已存在')])
    email = StringField('邮箱', [Email(), DataRequired(), Unique(User, User.email, '该邮箱已被占用')])
    password = PasswordField('密码', [DataRequired()])
    confirm = PasswordField('确认密码', [DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')


class URLForm(FlaskForm):
    urls = TextAreaField('', [DataRequired()], render_kw={'placeholder': '批量导入连接', 'rows': 5})
    search = StringField('', [Optional()], render_kw={'placeholder': '搜索过滤的字符'})
    use_regex = BooleanField('使用正则', [Optional()])
    submit = SubmitField('提取')


class RegexForm(FlaskForm):
    name = StringField('站点名称', [DataRequired()], render_kw={'placeholder': '如：Github trending'})
    site = StringField('站点URL', [DataRequired()], render_kw={'placeholder': '如：https://github.com/trending'})
    body = StringField('正则表达式', [DataRequired()], render_kw={'placeholder': '如：https://github.com/(?!(trending|login))\w+/\w+(?!/)'})
    submit = SubmitField('上传')

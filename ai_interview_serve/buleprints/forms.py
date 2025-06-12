import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel
from werkzeug.security import check_password_hash  # 加密


# 验证表单
class RegisterFrom(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])

    # 自定义验证
    # 1.邮箱是否已经被注册
    def validate_email(self, filed):
        email = filed.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    # 2.验证码是否正确
    # def validate_captcha(self, field):
    #     captcha = field.data
    #     email = self.email.data
    #     try:
    #         captcha_validate = redis_client.get("captcha").decode("utf-8")
    #         email_validate = redis_client.get("email").decode("utf-8")
    #     except (AttributeError, UnicodeDecodeError):
    #         captcha_validate = None
    #         email_validate = None
    #     if captcha != captcha_validate or email != email_validate:
    #         raise wtforms.ValidationError(message="邮箱或者验证码错误！")


class LoginFrom(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])

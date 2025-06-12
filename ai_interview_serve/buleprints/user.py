import os

from flask import Blueprint, request, session, jsonify, current_app
from exts import mail, db, api
from flask_mail import Message
from flask_restful import Resource, reqparse
from result import R
from status import SUCCESS, ERROR
from .forms import RegisterFrom, LoginFrom
from models import UserModel
import string
import random
import multiprocessing

bp = Blueprint("user", __name__, url_prefix="/user")
api.init_app(bp)


class UserResource(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = UserModel.query.get(user_id)
            return R(code=SUCCESS, message=None, data=user.to_dict())


api.add_resource(UserResource, '/')


@bp.route("/logout", methods=['GET'])
def logout():
    session.pop("user_id", None)
    return R(code=SUCCESS, message=None, data=None)


@bp.route("/login", methods=['POST'])
def login():
    json_data = request.get_json()
    form = LoginFrom()
    form.email.data = json_data.get('email')
    form.password.data = json_data.get('password')

    if form.validate():
        email = form.email.data
        password = form.password.data
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return R(code=ERROR, message="邮箱在数据库中不存在！", data=None)
        if user.password == password:
            session['user_id'] = user.id
            session['email'] = user.email
            return R(code=SUCCESS, message="登陆成功！", data=user.to_dict())
        else:
            return R(code=ERROR, message="密码错误！", data=None)
    else:
        return R(code=ERROR, message=form.errors, data=None)


@bp.route("/register", methods=['POST'])
def register():
    json_data = request.get_json()
    print(json_data)
    form = RegisterFrom()
    form.email.data = json_data.get('email')
    form.captcha.data = json_data.get('captcha')
    form.password.data = json_data.get('password')

    if form.validate():
        pwd = json_data.get("password")
        user = UserModel(email=json_data.get("email"),
                         password=pwd)
        db.session.add(user)
        db.session.commit()
        static_dir = os.path.join(current_app.root_path, 'static')
        upload_dir = os.path.join(static_dir, json_data.get('email'))

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            print(f"已创建目录: {upload_dir}")
        else:
            print(f"目录已存在: {upload_dir}")

        return R(code=SUCCESS, message="注册成功!", data=None)
    else:
        return R(code=ERROR, message=form.errors, data=None)


def send_email(email, captcha):
    message = Message(subject="平台验证码", recipients=[email], body=f"您的验证码是:{captcha}")
    mail.send(message)


@bp.route("/getCaptcha", methods=['GET'])
def get_captcha():
    email = request.args.get("email")
    source = string.digits * 4
    captcha = "".join(random.sample(source, 4))
    pool = multiprocessing.Pool(3)
    pool.apply_async(send_email(email, captcha))
    # 邮箱验证码存进redis里
    # redis_client.set("email", email)
    # redis_client.set("captcha", captcha)
    # redis_client.expire("email", 60)
    # redis_client.expire("captcha", 60)
    return R(code=SUCCESS, message="验证码发送成功,请查收！", data={"验证码": captcha})

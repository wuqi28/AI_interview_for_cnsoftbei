# 扩展件 这个文件的存在意义就是为了解决循环引用的问题
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_restful import Api

import config

db = SQLAlchemy()
mail = Mail()
api = Api()

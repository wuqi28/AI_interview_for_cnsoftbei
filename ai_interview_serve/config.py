import os

# 数据库的配置信息
HOSTNAME = "127.0.0.1"
PORT = 3306
DATABASE = "ai_interview"
USERNAME = "root"
PASSWORD = "root"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "857592710@qq.com"
MAIL_PASSWORD = "txstfqcatsvxbfif"
MAIL_DEFAULT_SENDER = "857592710@qq.com"

# session密钥
SECRET_KEY = os.urandom(24)

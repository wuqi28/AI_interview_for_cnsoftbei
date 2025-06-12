from flask import Flask
from flask_migrate import Migrate
import config
from flask_cors import CORS
from exts import db, mail
from buleprints.user import bp as user_bp
from buleprints.resume import bp as resume_bp
from buleprints.interview import bp as interview_bp
import models

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# 与app绑定
db.init_app(app)
mail.init_app(app)
CORS(app, supports_credentials=True)

# ORM映射
migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(interview_bp)


if __name__ == '__main__':
    app.run(debug=True)

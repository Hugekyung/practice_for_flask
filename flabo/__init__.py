from flask import Flask, request, render_template, abort

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

# 애플리케이션 팩토리 형태를 통해 규모 있는 플라스크 프로젝트를 만들 수 있다.
# 프로젝트 폴더 하위에 파일 한 개가 나와 있는 기본적인 형태의 경우 간단한 프로젝트에는 괜찮다.
# 하지만 프로젝트 규모가 커질 경우, 여러 곳에서 동시에 참조하는 순환참조 문제가 발생할 수 있다.
# 따라서 아래와 같은 형태로 app을 생성한다. 반드시 create_app이라는 이름으로 함수를 생성해야한다.
# 또한 "exprot FLASK_APP=폴더이름" 을 설정해야 정상적으로 플라스크를 띄울 수 있다.
def create_app(): # 애플리케이션 팩토리
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models # 순환참조 문제 때문에 create_app 함수 바깥에서 호출하면 안된다.

    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app



# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()

# if __name__ == '__main__':
#     app.run(debug=True)
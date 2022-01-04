from flask import Flask, request, render_template, abort
from .views import main_views

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

    '''@app.route('/')
    @app.route('/<name>')
    def hello_world(name='해찬'):
        # abort(404) # 에러 발생하기
        if request.method == "GET":
            return render_template('hello.html', name=name)
        else:
            return f"{request.method}: Bad Request!!"

    @app.route('/mypage')
    def my_page():
        return 'My Page!!'

    # 에러 페이지 커스터마이징: 404에러에 대한 페이지 커스터마이징
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('page_not_found.html'), 404 # 렌더링 해야 하는 에러 코드와 그에 대한 html 파일'''

    # 위의 긴 코드가 아래의 한 줄로 바뀌며 main_views.py에서 정보를 불러오는 형식이 적용됐다.
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
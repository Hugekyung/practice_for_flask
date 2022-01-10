from flask import Flask, request, render_template, abort
from flaskext.markdown import Markdown

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# 애플리케이션 팩토리 형태를 통해 규모 있는 플라스크 프로젝트를 만들 수 있다.
# 프로젝트 폴더 하위에 파일 한 개가 나와 있는 기본적인 형태의 경우 간단한 프로젝트에는 괜찮다.
# 하지만 프로젝트 규모가 커질 경우, 여러 곳에서 동시에 참조하는 순환참조 문제가 발생할 수 있다.
# 따라서 아래와 같은 형태로 app을 생성한다. 반드시 create_app이라는 이름으로 함수를 생성해야한다.
# 또한 "exprot FLASK_APP=폴더이름" 을 설정해야 정상적으로 플라스크를 띄울 수 있다.
def create_app(): # 애플리케이션 팩토리
    app = Flask(__name__)
    app.config.from_object(config)

    # markdown
    Markdown(app, extensions=['nl2br', 'fenced_code'])

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models # 순환참조 문제 때문에 create_app 함수 바깥에서 호출하면 안된다.

    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
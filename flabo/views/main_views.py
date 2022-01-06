from flask import Blueprint, request, render_template

from flabo.models import Question, Answer

'''블루프린트는 새로운 url이 추가될 때마다 __init__.py에서 create_app함수에 경로에 대한 코드를 작성해야 하는
번거로움을 해결하고자 할 때 사용하는 클래스다.'''
# url_prefix는 url앞에 기본으로 붙일 주소에 대한 설정값이다.
# 만약 url_prefix='/main'이라면, 기본 주소는 localhost:5000/main/ 이 된다.
bp = Blueprint('main', __name__, url_prefix='/')


# @bp.route('/')
# @bp.route('/<name>')
# def hello_world(name='해찬'):
#     # abort(404) # 에러 발생하기
#     if request.method == "GET":
#         return render_template('hello.html', name=name)
#     else:
#         return f"{request.method}: Bad Request!!"

@bp.route('/')
def index():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id) # get_or_404: 해당 데이터가 없는 경우 404 페이지 표시
    return render_template('question/question_detail.html', question=question)

# 에러 페이지 커스터마이징: 404에러에 대한 페이지 커스터마이징
@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404 # 렌더링 해야 하는 에러 코드와 그에 대한 html 파일
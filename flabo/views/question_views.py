from datetime import datetime
from flask import Blueprint, request, render_template, url_for, g
from werkzeug.utils import redirect

from flabo import db
from flabo.forms import QuestionForm, AnswerForm
from flabo.models import Question
from flabo.views.auth_views import login_required


bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id) # get_or_404: 해당 데이터가 없는 경우 404 페이지 표시
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    # form.validate_on_submit 함수는 전송된 폼 데이터의 정합성을 점검
    # 즉, 폼을 생성할 때 각 필드에 지정한 DataRequired() 같은 점검 항목에 이상이 없는지 확인
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, 
                            create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

# 에러 페이지 커스터마이징: 404에러에 대한 페이지 커스터마이징
@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404 # 렌더링 해야 하는 에러 코드와 그에 대한 html 파일
from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, render_template, url_for, g, flash
from werkzeug.utils import redirect

from flabo import db
from flabo.forms import QuestionForm, AnswerForm
from flabo.models import Question, Answer, User, question_voter
from flabo.views.auth_views import login_required


bp = Blueprint('question', __name__, url_prefix='/question')

# @bp.route('/list/')
# def _list():
#     page = request.args.get('page', type=int, default=1)  # 페이지
#     question_list = Question.query.order_by(Question.create_date.desc())
#     question_list = question_list.paginate(page, per_page=10)
#     return render_template('question/question_list.html', question_list=question_list)

@bp.route('/list/')
def _list():
    # 입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 정렬
    if so == 'recommend': # 추천순(추천 투표 많은 순)
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular': # 인기순(댓글 많은 순)
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query.outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:  # recent 최신순
        question_list = Question.query.order_by(Question.create_date.desc())

    # 조회
    # question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username).join(User, Answer.user_id == User.id).subquery()
        question_list = question_list.join(User).outerjoin(sub_query, sub_query.c.question_id == Question.id) \
                    .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()

    # 페이징
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, so=so)

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

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청 -> 수정하기 버튼을 누르고 들어간 페이지에서 저장하기 누를 때
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청 -> 수정하기 버튼을 누를 때
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

# 에러 페이지 커스터마이징: 404에러에 대한 페이지 커스터마이징
@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404 # 렌더링 해야 하는 에러 코드와 그에 대한 html 파일
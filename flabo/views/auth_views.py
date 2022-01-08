import functools
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from flabo import db
from flabo.forms import UserCreateForm, UserLoginForm
from flabo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# generate_password_hash 함수로 암호화한 데이터는 복호화할 수 없다
# 그래서 로그인할 때 입력받은 비밀번호는 암호화하여 저장된 비밀번호와 비교해야 한다
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request # before_app_request : 모든 라우트 함수보다 먼저 실행하게 하는 어노테이션
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None # g : 플라스크에서 제공하는 컨텍스트 변수
    else: # session 변수에 user_id값이 있으면 데이터베이스에서 이를 조회하여 g.user에 저장
        g.user = User.query.get(user_id) # g.user에는 User 객체가 저장된다

@bp.route('/logout/')
def logout():
    session.clear() # 세션의 모든 값을 삭제 즉, g.user = None
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
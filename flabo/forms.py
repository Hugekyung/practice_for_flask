from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=2, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])


class QuestionForm(FlaskForm): # FlaskForm 클래스를 상속받아야 한다
    # StringField(Label, validators)
    # validators는 검증을 위해 사용되는 도구로 필수 항목인지를 체크하는 DataRequired, 이메일인지를 체크하는 Email, 길이를 체크하는 Length등이 있다
    # 예를들어 필수값이면서 이메일이어야 하면 validators=[DataRequired('에러 메세지'), Email()] 과 같이 사용할 수 있다.
    subject = StringField('제목', validators=[DataRequired('제목을 작성해주세요.')]) # 글자 수 제한
    content = TextAreaField('내용', validators=[DataRequired('내용을 작성해주세요.')]) # 글자 수 제한 없음


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


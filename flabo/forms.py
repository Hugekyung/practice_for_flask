from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm): # FlaskForm 클래스를 상속받아야 한다
    # StringField(Label, validators)
    # validators는 검증을 위해 사용되는 도구로 필수 항목인지를 체크하는 DataRequired, 이메일인지를 체크하는 Email, 길이를 체크하는 Length등이 있다
    # 예를들어 필수값이면서 이메일이어야 하면 validators=[DataRequired(), Email()] 과 같이 사용할 수 있다.
    subject = StringField('제목', validators=[DataRequired()]) # 글자 수 제한
    content = TextAreaField('내용', validators=[DataRequired()]) # 글자 수 제한 없음
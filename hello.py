from flask import Flask, request, render_template, abort

app = Flask(__name__)

@app.route('/')
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
    return render_template('page_not_found.html'), 404 # 렌더링 해야 하는 에러 코드와 그에 대한 html 파일

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()

if __name__ == '__main__':
    app.run(debug=True)
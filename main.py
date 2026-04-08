from pages import *
from flask import Flask, render_template, request, redirect
from data import Data, pages_path
from flask_login import login_user
from login import *

app = Flask(__name__)
login_manager.init_app(app)


@app.route('/ru', methods=['POST', 'GET'])
@app.route('/main/ru', methods=['POST', 'GET'])
def main_page_ru():
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect('/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
    return return_main_page_ru()


def return_main_page_ru():
    data = Data(pages_path + 'main_ru.json')
    return create_main_page(data)


@app.route('/en', methods=['POST', 'GET'])
@app.route('/main/en', methods=['POST', 'GET'])
def main_page_en():
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect('/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
    return return_main_page_en()


def return_main_page_en():
    data = Data(pages_path + 'main_en.json')
    return create_main_page(data)


@app.route('/', methods=['GET'])
@app.route('/main', methods=['GET'])
def main_page():
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect('/ru')
    return redirect('/en')


# TODO: это после базы данных
'''@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)
'''

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)

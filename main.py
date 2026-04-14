from pages import *
from flask import Flask, request, redirect, abort
from data import TextData, pages_path, games_short_names_list
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
                case 'CS 2':
                    return redirect('/game/cs2/ru')
                case 'Escape From Tarkov':
                    return redirect('/game/eft/ru')
                case 'add_spot':
                    return redirect('/add_spot/ru')
    return return_main_page_ru()


def return_main_page_ru():
    data = TextData(pages_path + 'main_ru.json')
    return create_main_page(data)


@app.route('/en', methods=['POST', 'GET'])
@app.route('/main/en', methods=['POST', 'GET'])
def main_page_en():
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            print(btn_pressed)
            match btn_pressed:
                case 'change_lang':
                    return redirect('/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'CS 2':
                    return redirect('/game/cs2/en')
                case 'Escape From Tarkov':
                    return redirect('/game/eft/en')
                case 'add_spot':
                    return redirect('/add_spot/en')
    return return_main_page_en()


def return_main_page_en():
    data = TextData(pages_path + 'main_en.json')
    return create_main_page(data)


@app.route('/', methods=['GET'])
@app.route('/main', methods=['GET'])
def main_page():
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect('/ru')
    return redirect('/en')


def return_add_spot_page_en():
    data = TextData(pages_path + 'add_spot_en.json')
    return create_add_spot_page(data)


def return_add_spot_page_ru():
    data = TextData(pages_path + 'add_spot_ru.json')
    return create_add_spot_page(data)


@app.route('/add_spot', methods=['GET'])
def add_spot_page():
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect('/add_spot/ru')
    return redirect('/add_spot/en')


@app.route('/add_spot/en', methods=['POST', 'GET'])
def add_spot_page_en():
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect('/add_spot/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'send':
                    print('Sent!')  # TODO: Считать все данные с формы
                case 'to_main':
                    return redirect('/en')
    return return_add_spot_page_en()


@app.route('/add_spot/ru', methods=['POST', 'GET'])
def add_spot_page_ru():
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect('/add_spot/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'send':
                    print('Sent!')  # TODO: Считать все данные с формы
                case 'to_main':
                    return redirect('/ru')
    return return_add_spot_page_ru()


def return_game_info_page_en(short_name: str):
    data = TextData(pages_path + short_name + '_info_en.json')
    return create_game_info_page(data)


def return_game_info_page_ru(short_name: str):
    data = TextData(pages_path + short_name + '_info_ru.json')
    return create_game_info_page(data)


@app.route('/game/<string:game_short_name>/info', methods=['GET'])
def game_info_page(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/game/{game_short_name}/info/ru')
    return redirect(f'/game/{game_short_name}/info/en')


@app.route('/game/<string:game_short_name>/info/ru', methods=['POST', 'GET'])
def game_info_page_ru(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/game/{game_short_name}/info/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_game':
                    return redirect(f'/game/{game_short_name}/ru')
                case 'to_main':
                    return redirect('/ru')
    return return_game_info_page_ru(game_short_name)


@app.route('/game/<string:game_short_name>/info/en', methods=['POST', 'GET'])
def game_info_page_en(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/game/{game_short_name}/info/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_game':
                    return redirect(f'/game/{game_short_name}/en')
                case 'to_main':
                    return redirect('/en')
    return return_game_info_page_en(game_short_name)


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
    app.run(port=8080, host='127.0.0.1')

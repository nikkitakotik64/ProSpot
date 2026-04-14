from pages import *
from flask import Flask, request, redirect, abort
from data import TextData, pages_path, games_short_names_list, maps_dict
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


def return_game_page_en(short_name: str):
    data = TextData(pages_path + short_name + '_en.json')
    return create_game_page(data)


def return_game_page_ru(short_name: str):
    data = TextData(pages_path + short_name + '_ru.json')
    return create_game_page(data)


@app.route('/game/<string:game_short_name>', methods=['GET'])
def game_page(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/game/{game_short_name}/ru')
    return redirect(f'/game/{game_short_name}/en')


@app.route('/game/<string:game_short_name>/ru', methods=['POST', 'GET'])
def game_page_ru(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/game/{game_short_name}/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/ru')
    return return_game_page_ru(game_short_name)


@app.route('/game/<string:game_short_name>/en', methods=['POST', 'GET'])
def game_page_en(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/game/{game_short_name}/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/en')
    return return_game_page_en(game_short_name)


def return_guess_page_en(short_name: str):
    data = TextData(pages_path + short_name + '_guess_en.json')
    return create_game_page(data)


def return_guess_page_ru(short_name: str):
    data = TextData(pages_path + short_name + '_guess_ru.json')
    return create_game_page(data)


@app.route('/guess/<string:game_short_name>/<int:map_id>', methods=['GET'])
def guess_page(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 0 or map_id > len(maps_dict[game_short_name]):
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/guess/{game_short_name}/{map_id}/ru')
    return redirect(f'/guess/{game_short_name}/{map_id}/en')


@app.route('/guess/<string:game_short_name>/<int:map_id>/ru', methods=['POST', 'GET'])
def guess_page_ru(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 0 or map_id > len(maps_dict[game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/guess/{game_short_name}/{map_id}/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/ru')
                case 'to_game':
                    return redirect(f'/game/{game_short_name}/ru')
    return return_guess_page_ru(game_short_name)


@app.route('/guess/<string:game_short_name>/<int:map_id>/en', methods=['POST', 'GET'])
def guess_page_en(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 0 or map_id > len(maps_dict[game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/guess/{game_short_name}/{map_id}/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/en')
                case 'to_game':
                    return redirect(f'/game/{game_short_name}/en')
    return return_guess_page_en(game_short_name)


def return_learn_page_en(short_name: str, map_id: int):
    data = TextData(pages_path + 'learn_en.json')
    return create_learn_page(data, maps_dict[short_name][map_id])


def return_learn_page_ru(short_name: str, map_id: int):
    data = TextData(pages_path + 'learn_ru.json')
    return create_learn_page(data, maps_dict[short_name][map_id])


@app.route('/learn/<string:game_short_name>/<int:map_id>', methods=['GET'])
def learn_page(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict[game_short_name]):
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/learn/{game_short_name}/{map_id}/ru')
    return redirect(f'/learn/{game_short_name}/{map_id}/en')


@app.route('/learn/<string:game_short_name>/<int:map_id>/ru', methods=['POST', 'GET'])
def learn_page_ru(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict[game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/learn/{game_short_name}/{map_id}/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/ru')
                case 'to_game':
                    return redirect(f'/game/{game_short_name}/ru')
    return return_learn_page_ru(game_short_name, map_id)


@app.route('/learn/<string:game_short_name>/<int:map_id>/en', methods=['POST', 'GET'])
def learn_page_en(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict[game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/learn/{game_short_name}/{map_id}/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/en')
                case 'to_game':
                    return redirect(f'/game/{game_short_name}/en')
    return return_learn_page_en(game_short_name, map_id)


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

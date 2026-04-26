from pages import *
from flask import Flask, request, redirect, abort
from data import TextData, pages_path, games_short_names_list, maps_dict, \
    map_descriptions, maps_path, images_path, full_game_name, memory_images_path, db_data
from flask_login import login_user
from datetime import datetime
from PIL import Image
from login import *
from enum import Enum
from data_db import db_session
from data_db.users import User
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'mi_crytie_ochen1_dva_geniya_prosto'

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User,user_id)


class MapChoiceType(Enum):
    learn = 1
    guess = 2
    map = 3


map_choice_type_names = {1: 'learn', 2: 'guess', 3: 'map'}


@app.route('/ru', methods=['POST', 'GET'])
@app.route('/main/ru', methods=['POST', 'GET'])
def main_page_ru():
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect('/en')
            case 'autho':
               return redirect('/regist/ru')  # TODO
            case 'CS 2':
                return redirect('/cs2/ru')
            case 'Escape From Tarkov':
                return redirect('/eft/ru')
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
        match btn_pressed:
            case 'change_lang':
                return redirect('/ru')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'CS 2':
                return redirect('/cs2/en')
            case 'Escape From Tarkov':
                return redirect('/eft/en')
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


def return_add_spot_page_en(game: str | None = None, map_name: str | None = None,
                            pos: tuple[float, float] | None = None, name: str | None = None,
                            game_errors: list | None = None, map_errors: list | None = None,
                            spot_name_errors: list | None = None, file_errors: list | None = None):
    data = TextData(pages_path + 'add_spot_en.json')
    return create_add_spot_page(data, game, map_name, pos, name, game_errors, map_errors, spot_name_errors, file_errors)


def return_add_spot_page_ru(game: str | None = None, map_name: str | None = None,
                            pos: tuple[float, float] | None = None, name: str | None = None,
                            game_errors: list | None = None, map_errors: list | None = None,
                            spot_name_errors: list | None = None, file_errors: list | None = None):
    data = TextData(pages_path + 'add_spot_ru.json')
    return create_add_spot_page(data, game, map_name, pos, name, game_errors, map_errors, spot_name_errors, file_errors)


@app.route('/add_spot', methods=['GET'])
def add_spot_page():
    if False:
        abort(403)  # TODO: пользователь не авторизован
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect('/add_spot/ru')
    return redirect('/add_spot/en')


@app.route('/add_spot/en', methods=['POST', 'GET'])
def add_spot_page_en():
    if False:
        abort(403)  # TODO: пользователь не авторизован
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        game = request.form.get('game', None)
        if game not in games_list:
            game = None
            map_name = None
        else:
            map_name = request.form.get('map', None)
            if map_name not in maps_dict['en'][games_short_name_dict[game]]:
                map_name = None
        pos = (request.form.get('x_coord', None), request.form.get('y_coord', None))
        if pos[0] is None or pos[1] is None or not pos[0] or not pos[1]:
            pos = None
        name = request.form.get('spot_name', None)
        file = request.files.get('file', None)
        try:
            img = Image.open(file)
            img.verify()
            file.seek(0)
            file.save(images_path + 'test.jpg')
            file.seek(0)
        except:
            file = -1
        match btn_pressed:
            case 'change_lang':
                return redirect('/add_spot/ru')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'send':
                game_errors = []
                if game is None:
                    game_errors.append('game_not_chosen')
                map_errors = []
                if map_name is None:
                    map_errors.append('map_not_chosen')
                name_errors = []
                if not name:
                    name_errors.append('name_not_input')
                file_errors = []
                if file is None:
                    file_errors.append('file_not_chosen')
                elif file == -1:
                    file_errors.append('file_is_not_image')
                if game_errors or map_errors or name_errors or file_errors:
                    return return_add_spot_page_ru(game=game, map_name=map_name, pos=pos, name=name,
                                                   game_errors=game_errors, map_errors=map_errors,
                                                   spot_name_errors=name_errors, file_errors=file_errors)
                else:
                    filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
                    file.save(memory_images_path + filename)
                    db_data.save_added(game, map_name, pos, name, filename)
                    return redirect('/success/en')
            case 'to_main':
                return redirect('/en')
            case _:
                if not game:
                    try:
                        dct = dict()
                        for s in btn_pressed.split('; '):
                            key, value = s.split(': ')
                            dct[key] = value
                        game = dct.get('game', None)
                        map_name = dct.get('map_name', None)
                    except:
                        pass
        return return_add_spot_page_en(game=game, map_name=map_name, pos=pos, name=name)
    return return_add_spot_page_en()


@app.route('/add_spot/ru', methods=['POST', 'GET'])
def add_spot_page_ru():
    if False:
        abort(403)  # TODO: пользователь не авторизован
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        game = request.form.get('game', None)
        if game not in games_list:
            game = None
            map_name = None
        else:
            map_name = request.form.get('map', None)
            if map_name not in maps_dict['en'][games_short_name_dict[game]]:
                map_name = None
        pos = (request.form.get('x_coord', None), request.form.get('y_coord', None))
        if pos[0] is None or pos[1] is None or not pos[0] or not pos[1]:
            pos = None
        name = request.form.get('spot_name', None)
        file = request.files.get('file', None)
        try:
            img = Image.open(file)
            img.verify()
            file.seek(0)
            file.save(images_path + 'test.jpg')
            file.seek(0)
        except:
            file = -1
        match btn_pressed:
            case 'change_lang':
                return redirect('/add_spot/en')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'send':
                game_errors = []
                if game is None:
                    game_errors.append('game_not_chosen')
                map_errors = []
                if map_name is None:
                    map_errors.append('map_not_chosen')
                name_errors = []
                if not name:
                    name_errors.append('name_not_input')
                file_errors = []
                if file is None:
                    file_errors.append('file_not_chosen')
                elif file == -1:
                    file_errors.append('file_is_not_image')
                if game_errors or map_errors or name_errors or file_errors:
                    return return_add_spot_page_ru(game=game, map_name=map_name, pos=pos, name=name,
                                                   game_errors=game_errors, map_errors=map_errors,
                                                   spot_name_errors=name_errors, file_errors=file_errors)
                else:
                    filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
                    file.save(memory_images_path + filename)
                    db_data.save_added(game, map_name, pos, name, filename)
                    return redirect('/success/ru')
            case 'to_main':
                return redirect('/ru')
            case _:
                if not game:
                    try:
                        dct = dict()
                        for s in btn_pressed.split('; '):
                            key, value = s.split(': ')
                            dct[key] = value
                        game = dct.get('game', None)
                        map_name = dct.get('map_name', None)
                    except:
                        pass
        return return_add_spot_page_ru(game=game, map_name=map_name, pos=pos, name=name)
    return return_add_spot_page_ru()


def return_game_info_page_en(short_name: str):
    data = TextData(pages_path + short_name + '_info_en.json')
    return create_game_info_page(data, short_name)


def return_game_info_page_ru(short_name: str):
    data = TextData(pages_path + short_name + '_info_ru.json')
    return create_game_info_page(data, short_name)


@app.route('/<string:game_short_name>/info', methods=['GET'])
def game_info_page(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/{game_short_name}/info/ru')
    return redirect(f'/{game_short_name}/info/en')


@app.route('/<string:game_short_name>/info/ru', methods=['POST', 'GET'])
def game_info_page_ru(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/info/en')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_game':
                return redirect(f'/{game_short_name}/ru')
            case 'to_main':
                return redirect('/ru')
    return return_game_info_page_ru(game_short_name)


@app.route('/<string:game_short_name>/info/en', methods=['POST', 'GET'])
def game_info_page_en(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/info/ru')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_game':
                return redirect(f'/{game_short_name}/en')
            case 'to_main':
                return redirect('/en')
    return return_game_info_page_en(game_short_name)


def return_game_page_en(short_name: str):
    data = TextData(pages_path + short_name + '_en.json')
    return create_game_page(data, short_name)


def return_game_page_ru(short_name: str):
    data = TextData(pages_path + short_name + '_ru.json')
    return create_game_page(data, short_name)


@app.route('/<string:game_short_name>', methods=['GET'])
def game_page(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/{game_short_name}/ru')
    return redirect(f'/{game_short_name}/en')


@app.route('/<string:game_short_name>/ru', methods=['POST', 'GET'])
def game_page_ru(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/en')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/ru')
            case 'Гайд':
                return redirect(f'/{game_short_name}/info/ru')
            case 'Карты':
                return redirect(f'/{game_short_name}/map_choice/{MapChoiceType.map.value}/ru')
            case 'Испытание':
                return redirect(f'/{game_short_name}/map_choice/{MapChoiceType.guess.value}/ru')
            case 'Учить позиции':
                return redirect(f'/{game_short_name}/map_choice/{MapChoiceType.learn.value}/ru')
    return return_game_page_ru(game_short_name)


@app.route('/<string:game_short_name>/en', methods=['POST', 'GET'])
def game_page_en(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/ru')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/en')
            case 'Guide':
                return redirect(f'/{game_short_name}/info/en')
            case 'Maps':
                return redirect(f'/{game_short_name}/map_choice/{MapChoiceType.map.value}/en')
            case 'Challenge':
                return redirect(f'/{game_short_name}/map_choice/{MapChoiceType.guess.value}/en')
            case 'Learn spots':
                return redirect(f'/{game_short_name}/map_choice/{MapChoiceType.learn.value}/en')
    return return_game_page_en(game_short_name)


def return_guess_page_en(short_name: str, map_name: str, mode: GuessMode,
                      pos: tuple[float, float] | None = None, map_errors: list[str] | None = None,
                      time: str | None = None, spot_id: int | None = None):
    data = TextData(pages_path + short_name + '_guess_en.json')
    return create_guess_page(data, short_name, map_name, mode, pos, map_errors, time, spot_id)


def return_guess_page_ru(short_name: str, map_name: str, mode: GuessMode,
                      pos: tuple[float, float] | None = None, map_errors: list[str] | None = None,
                      time: str | None = None, spot_id: int | None = None):
    data = TextData(pages_path + short_name + '_guess_ru.json')
    return create_guess_page(data, short_name, map_name, mode, pos, map_errors, time, spot_id)


@app.route('/<string:game_short_name>/guess/<int:map_id>', methods=['GET'])
def guess_page(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 0 or map_id > len(maps_dict['ru'][game_short_name]):
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/{game_short_name}/guess/{map_id}/ru')
    return redirect(f'/{game_short_name}/guess/{map_id}/en')


@app.route('/<string:game_short_name>/guess/<int:map_id>/ru', methods=['POST', 'GET'])
def guess_page_ru(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 0 or map_id > len(maps_dict['ru'][game_short_name]):
        abort(404)
    map_name = maps_dict['ru'][game_short_name][map_id - 1] if map_id else 'Случайная'
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        pos_x, pos_y = request.form.get('x_coord', None), request.form.get('y_coord', None)
        time = request.form.get('timer', None)
        map_name = request.form.get('map', map_name)
        mode = request.form.get('mode', None)
        if mode is not None:
            if mode == '1':
                mode = GuessMode.start
            elif mode == '2':
                mode = GuessMode.end
            elif mode == '0':
                mode = GuessMode.guess
            else:
                mode = None
        spot_id = request.form.get('spot_id', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/guess/{map_id}/en')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/ru')
            case 'to_game':
                return redirect(f'/{game_short_name}/ru')
            case 'guess':
                match mode:
                    case GuessMode.start:
                        spot_id = db_data.generate_spot(game_short_name, map_name)
                        time = '00:00'
                        pos_x, pos_y = -1, -1
                        return return_guess_page_ru(game_short_name, map_name, GuessMode.guess, (pos_x, pos_y),
                                             [], time, spot_id)
                    case GuessMode.guess:
                        map_errors = []
                        if pos_x is None or pos_y is None or not pos_x or not pos_y:
                            map_errors.append('pos_not_chosen')
                            pos_x, pos_y = -1, -1
                        if map_errors:
                            return return_guess_page_ru(game_short_name, map_name, GuessMode.guess, (pos_x, pos_y),
                                                        map_errors, time, spot_id)
                        else:
                            return return_guess_page_ru(game_short_name, map_name, GuessMode.end, (pos_x, pos_y),
                                                        map_errors, time, spot_id)
                    case GuessMode.end:
                        spot_id = db_data.generate_spot(game_short_name, map_name)
                        time = '00:00'
                        pos_x, pos_y = -1, -1
                        return return_guess_page_ru(game_short_name, map_name, GuessMode.guess, (pos_x, pos_y),
                                             [], time, spot_id)
    return return_guess_page_ru(game_short_name, map_name, GuessMode.start)


@app.route('/<string:game_short_name>/guess/<int:map_id>/en', methods=['POST', 'GET'])
def guess_page_en(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 0 or map_id > len(maps_dict['en'][game_short_name]):
        abort(404)
    map_name = maps_dict['en'][game_short_name][map_id - 1] if map_id else 'Random'
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        pos_x, pos_y = request.form.get('x_coord', None), request.form.get('y_coord', None)
        time = request.form.get('timer', None)
        map_name = request.form.get('map', map_name)
        mode = request.form.get('mode', None)
        if mode is not None:
            if mode == '1':
                mode = GuessMode.start
            elif mode == '2':
                mode = GuessMode.end
            elif mode == '0':
                mode = GuessMode.guess
            else:
                mode = None
        spot_id = request.form.get('spot_id', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/guess/{map_id}/ru')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/en')
            case 'to_game':
                return redirect(f'/{game_short_name}/en')
            case 'guess':
                match mode:
                    case GuessMode.start:
                        spot_id = db_data.generate_spot(game_short_name, map_name)
                        time = '00:00'
                        pos_x, pos_y = -1, -1
                        return return_guess_page_en(game_short_name, map_name, GuessMode.guess, (pos_x, pos_y),
                                             [], time, spot_id)
                    case GuessMode.guess:
                        map_errors = []
                        if pos_x is None or pos_y is None or not pos_x or not pos_y:
                            map_errors.append('pos_not_chosen')
                            pos_x, pos_y = -1, -1
                        if map_errors:
                            return return_guess_page_en(game_short_name, map_name, GuessMode.guess, (pos_x, pos_y),
                                                        map_errors, time, spot_id)
                        else:
                            return return_guess_page_en(game_short_name, map_name, GuessMode.end, (pos_x, pos_y),
                                                        map_errors, time, spot_id)
                    case GuessMode.end:
                        spot_id = db_data.generate_spot(game_short_name, map_name)
                        time = '00:00'
                        pos_x, pos_y = -1, -1
                        return return_guess_page_en(game_short_name, map_name, GuessMode.guess, (pos_x, pos_y),
                                             [], time, spot_id)
    return return_guess_page_en(game_short_name, map_name, GuessMode.start)


def return_learn_page_en(short_name: str, map_id: int, spot: str | None = None,
                         pos: tuple[int, int] | None = None):
    data = TextData(pages_path + 'learn_en.json')
    if spot is None:
        spot = data.get_phrase('not_chosen')
    return create_learn_page(data, short_name, maps_dict['en'][short_name][map_id], spot, pos)


def return_learn_page_ru(short_name: str, map_id: int, spot: str | None = None,
                         pos: tuple[int, int] | None = None):
    data = TextData(pages_path + 'learn_ru.json')
    if spot is None:
        spot = data.get_phrase('not_chosen')
    return create_learn_page(data, short_name, maps_dict['ru'][short_name][map_id], spot, pos)


@app.route('/<string:game_short_name>/learn/<int:map_id>', methods=['GET'])
def learn_page(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict['ru'][game_short_name]):
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/{game_short_name}/learn/{map_id}/ru')
    return redirect(f'/{game_short_name}/learn/{map_id}/en')


@app.route('/<string:game_short_name>/learn/<int:map_id>/ru', methods=['POST', 'GET'])
def learn_page_ru(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict['ru'][game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/learn/{map_id}/en')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/ru')
            case 'to_game':
                return redirect(f'/{game_short_name}/ru')
        pos_x, pos_y = request.form.get('x_coord', None), request.form.get('y_coord', None)
        spot = request.form.get('spot', None)
        if not pos_x or not pos_y:
            pos = None
        else:
            pos = [int(pos_x), int(pos_y)]
        return return_learn_page_ru(game_short_name, map_id - 1, spot, pos)
    return return_learn_page_ru(game_short_name, map_id - 1)


@app.route('/<string:game_short_name>/learn/<int:map_id>/en', methods=['POST', 'GET'])
def learn_page_en(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict['en'][game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/learn/{map_id}/ru')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/en')
            case 'to_game':
                return redirect(f'/{game_short_name}/en')
        pos_x, pos_y = request.form.get('x_coord', None), request.form.get('y_coord', None)
        spot = request.form.get('spot', None)
        if not pos_x or not pos_y:
            pos = None
        else:
            pos = [int(pos_x), int(pos_y)]
        return return_learn_page_en(game_short_name, map_id - 1, spot, pos)
    return return_learn_page_en(game_short_name, map_id - 1)


def return_map_choice_page_en(short_name: str, is_guess: bool):
    data = TextData(pages_path + 'map_choice_en.json')
    return create_map_choice_page(data, (['Random'] if is_guess else []) + maps_dict['en'][short_name],
                                  full_game_name[short_name])


def return_map_choice_page_ru(short_name: str, is_guess: bool):
    data = TextData(pages_path + 'map_choice_ru.json')
    return create_map_choice_page(data, (['Случайная'] if is_guess else []) + maps_dict['ru'][short_name],
                                  full_game_name[short_name])


@app.route('/<string:game_short_name>/map_choice/<int:map_choice_type>', methods=['GET'])
def map_choice_page(game_short_name: str, map_choice_type: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_choice_type not in map_choice_type_names.keys():
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/{game_short_name}/map_choice/{map_choice_type}/ru')
    return redirect(f'/{game_short_name}/map_choice/{map_choice_type}/en')


@app.route('/<string:game_short_name>/map_choice/<int:map_choice_type>/ru', methods=['POST', 'GET'])
def map_choice_page_ru(game_short_name: str, map_choice_type: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_choice_type not in map_choice_type_names.keys():
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/map_choice/{map_choice_type}/en')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/ru')
            case 'to_game':
                return redirect(f'/{game_short_name}/ru')
            case 'Случайная':
                return redirect(f'/{game_short_name}/guess/0/ru')
            case _:
                if btn_pressed in maps_dict['ru'][game_short_name]:
                    ind = maps_dict['ru'][game_short_name].index(btn_pressed) + 1
                    match map_choice_type:
                        case MapChoiceType.map.value:
                            return redirect(f'/{game_short_name}/map/{ind}/ru')
                        case MapChoiceType.guess.value:
                            return redirect(f'/{game_short_name}/guess/{ind}/ru')
                        case MapChoiceType.learn.value:
                            return redirect(f'/{game_short_name}/learn/{ind}/ru')
    return return_map_choice_page_ru(game_short_name, map_choice_type == MapChoiceType.guess.value)


@app.route('/<string:game_short_name>/map_choice/<int:map_choice_type>/en', methods=['POST', 'GET'])
def map_choice_page_en(game_short_name: str, map_choice_type: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_choice_type not in map_choice_type_names.keys():
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/map_choice/{map_choice_type}/ru')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/en')
            case 'to_game':
                return redirect(f'/{game_short_name}/en')
            case 'Random':
                return redirect(f'/{game_short_name}/guess/0/en')
            case _:
                if btn_pressed in maps_dict['en'][game_short_name]:
                    ind = maps_dict['en'][game_short_name].index(btn_pressed) + 1
                    match map_choice_type:
                        case MapChoiceType.map.value:
                            return redirect(f'/{game_short_name}/map/{ind}/en')
                        case MapChoiceType.guess.value:
                            return redirect(f'/{game_short_name}/guess/{ind}/en')
                        case MapChoiceType.learn.value:
                            return redirect(f'/{game_short_name}/learn/{ind}/en')
    return return_map_choice_page_en(game_short_name, map_choice_type == MapChoiceType.guess.value)


def return_map_page_en(map_name: str, short_game_name: str, description_file: str):
    data = TextData(pages_path + 'map_en.json')
    return create_map_page(data, map_name, short_game_name, description_file)


def return_map_page_ru(map_name: str, short_game_name: str, description_file: str):
    data = TextData(pages_path + 'map_ru.json')
    return create_map_page(data, map_name, short_game_name, description_file)


@app.route('/<string:game_short_name>/map/<int:map_id>', methods=['GET'])
def map_page(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict['ru'][game_short_name]):
        abort(404)
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect(f'/{game_short_name}/map/{map_id}/ru')
    return redirect(f'/{game_short_name}/map/{map_id}/en')


@app.route('/<string:game_short_name>/map/<int:map_id>/ru', methods=['POST', 'GET'])
def map_page_ru(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict['ru'][game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/map/{map_id}/en')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/ru')
            case 'to_game':
                return redirect(f'/{game_short_name}/ru')
    return return_map_page_ru(maps_dict['ru'][game_short_name][map_id - 1], game_short_name,
                              maps_path + map_descriptions['ru'][game_short_name][map_id - 1])


@app.route('/<string:game_short_name>/map/<int:map_id>/en', methods=['POST', 'GET'])
def map_page_en(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict['en'][game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'change_lang':
                return redirect(f'/{game_short_name}/map/{map_id}/ru')
            case 'autho':
                print('Авторизация пока недоступна')  # TODO
            case 'to_main':
                return redirect('/en')
            case 'to_game':
                return redirect(f'/{game_short_name}/en')
    return return_map_page_en(maps_dict['en'][game_short_name][map_id - 1], game_short_name,
                              maps_path + map_descriptions['en'][game_short_name][map_id - 1])


@app.route('/success/ru', methods=['POST', 'GET'])
def return_success_send_page_ru():
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'to_main':
                return redirect('/ru')
            case 'change_lang':
                return redirect('/success/en')
            case 'autho':
                print('')  # TODO
    data = TextData(pages_path + 'success_ru.json')
    return create_send_success_page(data)


@app.route('/success/en', methods=['POST', 'GET'])
def return_success_send_page_en():
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        match btn_pressed:
            case 'to_main':
                return redirect('/en')
            case 'change_lang':
                return redirect('/success/ru')
            case 'autho':
                print('')  # TODO
    data = TextData(pages_path + 'success_en.json')
    return create_send_success_page(data)

@app.route("/regist/ru", methods=["POST", "GET"])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,

        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/regist/ru')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/autho/ru', methods=['POST', 'GET'])
def create_autho_page_ru():
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('authorizarion.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('authorization.html', title='Авторизация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/users.sqlite")
    app.run(port=8080, host='127.0.0.1')

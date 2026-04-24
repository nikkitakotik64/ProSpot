from pages import *
from flask import Flask, request, redirect, abort
from data import TextData, pages_path, games_short_names_list, maps_dict, games_dict, games_with_spots, \
    map_descriptions, maps_path, SpotData, images_path
from flask_login import login_user
from PIL import Image
from login import *

app = Flask(__name__)
login_manager.init_app(app)

map_choice_types = {1: 'learn', 2: 'guess', 3: 'map'}


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
        if btn_pressed:
            print(btn_pressed)
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
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect('/add_spot/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'send':
                    pass  # TODO
                case 'to_main':
                    return redirect('/en')
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
            file.save(images_path + 'test.jpg') # TODO: вставить путь
        except:
            file = -1
        if btn_pressed:
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
                        # TODO: сохранить всё
                        return redirect('/')  # TODO страничка, что всё успешно отправлено
                case 'to_main':
                    return redirect('/ru')
        return return_add_spot_page_ru(game=game, map_name=map_name, pos=pos, name=name)
    return return_add_spot_page_ru()


def return_game_info_page_en(short_name: str):
    data = TextData(pages_path + short_name + '_info_en.json')
    return create_game_info_page(data)


def return_game_info_page_ru(short_name: str):
    data = TextData(pages_path + short_name + '_info_ru.json')
    return create_game_info_page(data)


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
        if btn_pressed:
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
        if btn_pressed:
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
    return create_game_page(data)


def return_game_page_ru(short_name: str):
    data = TextData(pages_path + short_name + '_ru.json')
    return create_game_page(data)


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
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/ru')
    return return_game_page_ru(game_short_name)


@app.route('/<string:game_short_name>/en', methods=['POST', 'GET'])
def game_page_en(game_short_name: str):
    if game_short_name not in games_short_names_list:
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/ru')
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
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/guess/{map_id}/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/ru')
                case 'to_game':
                    return redirect(f'/{game_short_name}/ru')
    return return_guess_page_ru(game_short_name)


@app.route('/<string:game_short_name>/guess/<int:map_id>/en', methods=['POST', 'GET'])
def guess_page_en(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 0 or map_id > len(maps_dict['en'][game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/guess/{map_id}/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/en')
                case 'to_game':
                    return redirect(f'/{game_short_name}/en')
    return return_guess_page_en(game_short_name)


def return_learn_page_en(short_name: str, map_id: int):
    data = TextData(pages_path + 'learn_en.json')
    return create_learn_page(data, maps_dict['en'][short_name][map_id])


def return_learn_page_ru(short_name: str, map_id: int):
    data = TextData(pages_path + 'learn_ru.json')
    return create_learn_page(data, maps_dict['ru'][short_name][map_id])


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
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/learn/{map_id}/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/ru')
                case 'to_game':
                    return redirect(f'/{game_short_name}/ru')
    return return_learn_page_ru(game_short_name, map_id)


@app.route('/<string:game_short_name>/learn/<int:map_id>/en', methods=['POST', 'GET'])
def learn_page_en(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict['en'][game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/learn/{map_id}/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/en')
                case 'to_game':
                    return redirect(f'/{game_short_name}/en')
    return return_learn_page_en(game_short_name, map_id)


def return_map_choice_page_en(short_name: str, is_guess: bool):
    data = TextData(pages_path + 'map_choice_en.json')
    return create_map_choice_page(data, (['Random'] if is_guess else []) + maps_dict['en'][short_name],
                                  games_dict[short_name])


def return_map_choice_page_ru(short_name: str, is_guess: bool):
    data = TextData(pages_path + 'map_choice_ru.json')
    return create_map_choice_page(data, (['Случайная'] if is_guess else []) + maps_dict['ru'][short_name],
                                  games_dict[short_name])


@app.route('/<string:game_short_name>/map_choice/<int:map_choice_type>', methods=['GET'])
def map_choice_page(game_short_name: str, map_choice_type: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_choice_type not in map_choice_types.keys():
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
    if map_choice_type not in map_choice_types.keys():
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/map_choice/{map_choice_type}/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/ru')
                case 'to_game':
                    return redirect(f'/{game_short_name}/ru')
    return return_map_choice_page_ru(game_short_name, map_choice_type == 2)


@app.route('/<string:game_short_name>/map_choice/<int:map_choice_type>/en', methods=['POST', 'GET'])
def map_choice_page_en(game_short_name: str, map_choice_type: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_choice_type not in map_choice_types.keys():
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/map_choice/{map_choice_type}/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/en')
                case 'to_game':
                    return redirect(f'/{game_short_name}/en')
    return return_map_choice_page_en(game_short_name, map_choice_type == 2)


def return_map_page_en(map_name: str, is_have_spots: bool, description_file: str):
    data = TextData(pages_path + 'map_en.json')
    return create_map_page(data, map_name, is_have_spots, description_file)


def return_map_page_ru(map_name: str, is_have_spots: bool, description_file: str):
    data = TextData(pages_path + 'map_ru.json')
    return create_map_page(data, map_name, is_have_spots, description_file)


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
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/map/{map_id}/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/ru')
                case 'to_game':
                    return redirect(f'/{game_short_name}/ru')
    return return_map_page_ru(maps_dict['ru'][game_short_name][map_id], game_short_name in games_with_spots,
                              maps_path + map_descriptions['ru'][game_short_name][map_id])


@app.route('/<string:game_short_name>/map/<int:map_id>/en', methods=['POST', 'GET'])
def map_page_en(game_short_name: str, map_id: int):
    if game_short_name not in games_short_names_list:
        abort(404)
    if map_id < 1 or map_id > len(maps_dict['en'][game_short_name]):
        abort(404)
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect(f'/{game_short_name}/map/{map_id}/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/en')
                case 'to_game':
                    return redirect(f'/{game_short_name}/en')
    return return_map_page_ru(maps_dict['en'][game_short_name][map_id], game_short_name in games_with_spots,
                              maps_path + map_descriptions['en'][game_short_name][map_id])


def return_moder_page_en():
    data = TextData(pages_path + 'moder_en.json')
    spot_info = SpotData()
    return create_moder_page(data, spot_info)


def return_moder_page_ru():
    data = TextData(pages_path + 'moder_ru.json')
    spot_info = SpotData()
    return create_moder_page(data, spot_info)


@app.route('/moder', methods=['GET'])
def moder_page():
    if True:
        abort(403)  # не админ
    request.accept_languages.best_match(['ru', 'en'])
    lang = request.accept_languages.best
    if lang == 'ru-RU':
        return redirect('/moder/ru')
    return redirect('/moder/en')


@app.route('/moder/en', methods=['POST', 'GET'])
def moder_page_en():
    if True:
        abort(403)  # не админ
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect('/moder/ru')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/en')
    return return_add_spot_page_en()


@app.route('/moder/ru', methods=['POST', 'GET'])
def moder_page_ru():
    if True:
        abort(403)  # не админ
    if request.method == 'POST':
        btn_pressed = request.form.get('btn', None)
        if btn_pressed:
            match btn_pressed:
                case 'change_lang':
                    return redirect('/moder/en')
                case 'autho':
                    print('Авторизация пока недоступна')  # TODO
                case 'to_main':
                    return redirect('/ru')
    return return_add_spot_page_ru()


# TODO: это после базы данных
'''
@app.route('/login')
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

# узнать, что пользователь закрыл страницу
# пока пусть тут полежит на всякий
'''
<script>
    window.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
            // Данные, которые хотим передать (например, ID сессии)
            const data = new FormData();
            data.append('status', 'left');

            // Отправляем запрос на Flask
            navigator.sendBeacon('/on_page_close', data);
        }
    });
</script>
'''

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

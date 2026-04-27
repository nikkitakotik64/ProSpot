from data import games_list, TextData, maps_dict, games_dict, games_short_name_dict, games_with_spots, db_data
from flask import render_template
from enum import Enum
from data_db.db_functions import is_authorized, get_current_user_name, get_user_info, get_current_user_id

title = 'ProSpot'


class PagesType(Enum):
    main = 0
    without_game_btn = 1
    with_game_btn = 2


class GuessMode(Enum):
    guess = 0
    start = 1
    end = 2


def create_main_page(data: TextData) -> str:
    if is_authorized():
        autho_text = get_current_user_name()
    else:
        autho_text = data.get_autho_btn_text()
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=autho_text,
                           change_lang_btn_text=data.get_another_lang(),
                           type=PagesType.main.value,
                           tech_info=data.get_phrase('tech_info'),
                           btn_list=games_list,
                           button_count=5,
                           add_spot_btn_text=data.get_phrase('add_spot_button'))


def create_add_spot_page(data: TextData, game: str | None, map_name: str | None,
                         pos: tuple[float, float] | None, name: str | None, game_errors: list | None,
                         map_errors: list | None, spot_name_errors: list | None, file_errors: list | None) -> str:
    map_image = 'None'
    if is_authorized():
        autho_text = get_current_user_name()
    else:
        autho_text = data.get_autho_btn_text()
    if game is not None:
        if map_name is not None:
            map_image = db_data.get_map_image(games_short_name_dict[game], map_name)
            maps = [map_name]
            for mp in maps_dict[data.get_lang()][games_short_name_dict[game]]:
                if mp != map_name:
                    maps.append(mp)
            maps.append(data.get_phrase('select_map_text'))
            if pos is not None:
                pos_x, pos_y = pos
            else:
                pos_x, pos_y = -1, -1
        else:
            maps = [data.get_phrase('select_map_text')] + maps_dict[data.get_lang()][games_short_name_dict[game]]
            pos_x, pos_y = -1, -1
        games = [game]
        for g in games_list:
            if g != game:
                games.append(g)
        games.append(data.get_phrase('select_game_text'))
    else:
        maps = [data.get_phrase('select_map_text')]
        games = [data.get_phrase('select_game_text'), *games_list]
        pos_x, pos_y = -1, -1
    if name is None:
        name = ''
    if game_errors is None:
        game_errors = list()
    else:
        for ind in range(len(game_errors)):
            game_errors[ind] = data.get_phrase(game_errors[ind])
    if map_errors is None:
        map_errors = list()
    else:
        for ind in range(len(map_errors)):
            map_errors[ind] = data.get_phrase(map_errors[ind])
    if spot_name_errors is None:
        spot_name_errors = list()
    else:
        for ind in range(len(spot_name_errors)):
            spot_name_errors[ind] = data.get_phrase(spot_name_errors[ind])
    if file_errors is None:
        file_errors = list()
    else:
        for ind in range(len(file_errors)):
            file_errors[ind] = data.get_phrase(file_errors[ind])
    return render_template('add_spot.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=autho_text,
                           change_lang_btn_text=data.get_another_lang(),
                           type=PagesType.without_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           tech_info=data.get_phrase('tech_info'),
                           games=games,
                           maps=maps,
                           map_image=map_image,
                           pos_x=pos_x,
                           pos_y=pos_y,
                           send_btn_txt=data.get_phrase('send_btn_text'),
                           name=name,
                           input_placeholder=data.get_phrase('input_name_text'),
                           game_errors=game_errors,
                           map_errors=map_errors,
                           spot_name_errors=spot_name_errors,
                           file_errors=file_errors)


def create_game_info_page(data: TextData, game: str) -> str:
    game_image = db_data.get_game_image(game)
    if is_authorized():
        autho_text = get_current_user_name()
    else:
        autho_text = data.get_autho_btn_text()
    return render_template('game_info_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=autho_text,
                           change_lang_btn_text=data.get_another_lang(),
                           type=PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           tech_info=data.get_phrase('tech_info'),
                           game_title=data.get_phrase('header'),
                           game_image=game_image,
                           game_name=games_dict[game],
                           game_description=data.get_phrase('text'),
                           add_spot_btn_text=data.get_phrase('add_spot_button'),)


def create_game_page(data: TextData, game: str) -> str:
    btn_list = [data.get_phrase('guide_btn'), data.get_phrase('maps_btn'), data.get_phrase('challenge_btn')]
    if game in games_with_spots:
        btn_list.append(data.get_phrase('learn_btn'))
    if is_authorized():
        autho_text = get_current_user_name()
    else:
        autho_text = data.get_autho_btn_text()
    return render_template('game_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=autho_text,
                           change_lang_btn_text=data.get_another_lang(),
                           type=PagesType.without_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           tech_info=data.get_phrase('tech_info'),
                           game_title=data.get_phrase('header'),
                           game_name=games_dict[game],
                           add_spot_btn_text=data.get_phrase('add_spot_button'),
                           btn_list=btn_list,
                           button_count=len(btn_list))


def create_guess_page(data: TextData, game: str, map_name: str, mode: GuessMode,
                      pos: tuple[float, float] | None, map_errors: list[str] | None, time: str | None,
                      spot_id: int | None) -> str:
    if is_authorized():
        autho_text = get_current_user_name()
    else:
        autho_text = data.get_autho_btn_text()
    maps = [map_name]
    if map_name != data.get_phrase('random_map'):
        maps.append(data.get_phrase('random_map'))
    for mp in maps_dict[data.get_lang()][game]:
        if mp != map_name:
            maps.append(mp)
    if mode == GuessMode.start:
        map_errors = []
        guess_text = data.get_phrase('start')
        pos_x, pos_y = -1, -1
        true_pos_x, true_pos_y = -1, -1
        curr_map_name = None
        spot_name = None
        accuracy = None
        spot_image = 'None'
        map_image = 'None'
    elif mode == GuessMode.guess:
        if time is None:
            raise TypeError('Guess mode without time')
        if spot_id is None:
            raise TypeError('Guess mode without spot_id')
        curr_map_name, *_ = db_data.get_spot(spot_id)
        if pos is not None:
            pos_x, pos_y = pos
        else:
            pos_x, pos_y = -1, -1
        true_pos_x, true_pos_y = -1, -1
        guess_text = data.get_phrase('guess')
        spot_name = None
        accuracy = None
        spot_image = db_data.get_spot_image(spot_id)
        map_image = db_data.get_map_image(game, curr_map_name)
    else:
        if time is None:
            raise TypeError('End mode without time')
        if spot_id is None:
            raise TypeError('End mode without spot_id')
        if pos is None:
            raise TypeError('End mode without pos')
        curr_map_name, true_pos_x, true_pos_y, spot_name = db_data.get_spot(spot_id)
        pos_x, pos_y = pos
        guess_text = data.get_phrase('next')
        accuracy = db_data.get_accuracy(game, curr_map_name, (pos_x, pos_y), (true_pos_x, true_pos_y))
        spot_image = db_data.get_spot_image(spot_id)
        map_image = db_data.get_map_image(game, curr_map_name)
        if is_authorized():
            count_games, score = get_user_info(user_id=get_current_user_id())
            count_games += 1
            score += accuracy
            # TODO: сохранить
    if map_errors is None:
        map_errors = list()
    else:
        for ind in range(len(map_errors)):
            map_errors[ind] = data.get_phrase(map_errors[ind])
    return render_template('guess_page.html',
                           lang=data.get_lang(),
                           title=title,
                           header=data.get_phrase('header'),
                           autho_btn_text=autho_text,
                           change_lang_btn_text=data.get_another_lang(),
                           type=PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           tech_info=data.get_phrase('tech_info'),
                           maps=maps,
                           pos_x=pos_x,
                           pos_y=pos_y,
                           map_errors=map_errors,
                           map_text=data.get_phrase('map'),
                           map_name=map_name,
                           time_text=data.get_phrase('time'),
                           time=time,
                           guess_text=guess_text,
                           map_image=map_image,
                           mode=mode.value,
                           curr_map_name=curr_map_name,
                           spot_id=spot_id,
                           spot_image=spot_image,
                           pos_text=data.get_phrase('pos'),
                           accuracy_text=data.get_phrase('accuracy'),
                           spot_name=spot_name,
                           accuracy=accuracy,
                           true_pos_x=true_pos_x,
                           true_pos_y=true_pos_y,)



def create_learn_page(data: TextData, game: str, map_name: str, spot: str, pos: tuple[int, int] | None) -> str:
    if is_authorized():
        autho_text = get_current_user_name()
    else:
        autho_text = data.get_autho_btn_text()
    radius = db_data.get_radius(game, map_name)
    spots = [spot]
    true_pos_x, true_pos_y = -1, -1
    positions = list()
    if pos is None:
        pos = [-1, -1]
    for spot_name, sp_pos_x, sp_pos_y in db_data.get_spots(game, map_name):
        positions.append([sp_pos_x, sp_pos_y])
        if pos == [-1, -1] or ((sp_pos_x - pos[0]) ** 2 + (sp_pos_y - pos[1]) ** 2) ** 0.5 <= radius:
            if spot_name != spot:
                spots.append(spot_name)
            else:
                true_pos_x, true_pos_y = sp_pos_x, sp_pos_y
        else:
            if spot_name == spot:
                spots[0] = data.get_phrase('not_chosen')
    if spots[0] != data.get_phrase('not_chosen'):
        images = db_data.get_images(game, map_name, spot)
    else:
        images = []
    map_image = db_data.get_map_image(game, map_name)
    return render_template('learn_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=autho_text,
                           change_lang_btn_text=data.get_another_lang(),
                           type=PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           tech_info=data.get_phrase('tech_info'),
                           radius=radius,
                           map_image=map_image,
                           spots=spots,
                           map_name=map_name,
                           images=images,
                           positions=positions,
                           pos_x=pos[0],
                           pos_y=pos[1],
                           true_pos_x=true_pos_x,
                           true_pos_y=true_pos_y,
                           header_start=data.get_phrase('header_start'),)


def create_map_choice_page(data: TextData, maps: list[str], game_name: str) -> str:
    if is_authorized():
        autho_text = get_current_user_name()
    else:
        autho_text = data.get_autho_btn_text()
    return render_template('map_choice.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=autho_text,
                           change_lang_btn_text=data.get_another_lang(),
                           type=PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           tech_info=data.get_phrase('tech_info'),
                           btn_list=maps,
                           button_count=5,
                           game_name=game_name,
                           subheader=data.get_phrase('choice'))


def create_map_page(data: TextData, map_name: str, game: str, description_file: str) -> str:
    if is_authorized():
        autho_text = get_current_user_name()
    else:
        autho_text = data.get_autho_btn_text()
    map_image = db_data.get_map_image(game, map_name)
    with open(description_file, 'r') as f:
        description = f.readlines()
    return render_template('map_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=autho_text,
                           change_lang_btn_text=data.get_another_lang(),
                           type=PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           game_name=games_dict[game],
                           map_name=map_name,
                           map_image=map_image,
                           map_description=description,
                           add_spot_btn_text=data.get_phrase('add_spot_button'),
                           tech_info=data.get_phrase('tech_info'))


def create_send_success_page(data: TextData) -> str:
    if is_authorized():
        autho_text = get_current_user_name()
    else:
        autho_text = data.get_autho_btn_text()
    return render_template('send_success_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=autho_text,
                           change_lang_btn_text=data.get_another_lang(),
                           type=PagesType.main.value,
                           tech_info=data.get_phrase('tech_info'),
                           to_main_btn_text=data.get_to_main_btn_text(),
                           success_text=data.get_phrase('success_text'))

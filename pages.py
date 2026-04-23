from click import pass_obj
from data import games_list, TextData, SpotData, maps_dict, games_short_names_list, games_short_name_dict
from flask import render_template
from enum import Enum

title = 'ProSpot'


class PagesType(Enum):
    main = 0
    without_game_btn = 1
    with_game_btn = 2


def create_main_page(data: TextData) -> str:
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.main.value,
                           tech_info=data.get_phrase('tech_info'),
                           btn_list=games_list,
                           button_count=5,
                           add_spot_btn_text=data.get_phrase('add_spot_button'))


def create_add_spot_page(data: TextData, game: str | None, map_name: str | None,
                         pos: tuple[float, float] | None, name: str | None) -> str:
    # TODO: надо чтобы картинка карты бралась из бд
    if game is not None:
        if map_name is not None:
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
    return render_template('add_spot.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.without_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           tech_info=data.get_phrase('tech_info'),
                           games=games,
                           maps=maps,
                           map_image='favicon.jpg',
                           pos_x=pos_x,
                           pos_y=pos_y,
                           send_btn_txt=data.get_phrase('send_btn_text'),
                           name=name)


def create_game_info_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('base_template.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           tech_info=data.get_phrase('tech_info'))


def create_game_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('base_template.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.without_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           tech_info=data.get_phrase('tech_info'))


def create_guess_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('base_template.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           tech_info=data.get_phrase('tech_info'))


def create_learn_page(data: TextData, map_name: str) -> str:  # TODO: добавить форму
    return render_template('base_template.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           tech_info=data.get_phrase('tech_info'))


def create_map_choice_page(data: TextData, maps: list[str], game_name: str) -> str:  # TODO: добавить форму
    return render_template('base_template.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           tech_info=data.get_phrase('tech_info'))


def create_map_page(data: TextData, map_name: str, is_have_spots: bool,
                    description_file: str) -> str:  # TODO: добавить форму
    return render_template('base_template.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           to_game_btn_text=data.get_to_game_btn_text(),
                           tech_info=data.get_phrase('tech_info'))


def create_moder_page(data: TextData, spot_info: SpotData) -> str:  # TODO: добавить форму
    return render_template('base_template.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.without_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           tech_info=data.get_phrase('tech_info'))


def create_account_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('base_template.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text=data.get_autho_btn_text(),
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.without_game_btn.value,
                           to_main_btn_text=data.get_to_main_btn_text(),
                           tech_info=data.get_phrase('tech_info'))

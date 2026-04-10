from data import games_list, TextData
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
                           autho_btn_text='Авторизация',  # TODO
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.main.value,
                           tech_info=data.get_phrase('tech_info'))


def create_add_spot_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.without_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))


def create_game_info_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))


def create_game_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.without_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))


def create_guess_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))


def create_learn_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))


def create_map_choice_to_learn_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))


def create_map_choice_to_guess_page(data: TextData) -> str:  # TODO: добавить форму
    # TODO: добавить кнопку Random
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))


def create_map_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.with_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))


def create_moder_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.without_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))


def create_account_page(data: TextData) -> str:  # TODO: добавить форму
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=title,
                           autho_btn_text='Авторизация',
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.without_game_btn.value,
                           tech_info=data.get_phrase('tech_info'))

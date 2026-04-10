from text_data import games_list, TextData, templates_path
from flask import render_template
from enum import Enum


class PagesType(Enum):
    main = 0
    games = 1
    another = 2


def create_main_page(data: TextData) -> str:
    return render_template('main_page.html',
                           lang=data.get_lang(),
                           title=data.get_phrase('title'),
                           autho_btn_text='Авторизация',  # TODO
                           change_lang_btn_text=data.get_another_lang(),
                           type = PagesType.main.value,
                           tech_info=data.get_phrase('tech_info'))

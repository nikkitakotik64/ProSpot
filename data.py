import json
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/'
pages_path = path + 'static/pages/'
templates_path = path + 'templates/'

games_list = ('CS 2', 'Escape From Tarkov')
games_short_names_list = ('cs2', 'eft')
maps_dict = {'cs2': ['', '', ''], 'eft': ['', '', '']}
games_dict = {'cs2': 'CS 2', 'eft': 'Escape From Tarkov'}


class TextData:
    def __init__(self, text_filename: str) -> None:
        with open(text_filename, 'r', encoding='utf-8') as text_file:
            self.text_data = json.load(text_file)

    def get_phrase(self, key: str) -> str:
        return self.text_data[key]

    def get_lang(self) -> str:
        return self.text_data['lang']

    def get_another_lang(self) -> str:
        return 'ru' if self.get_lang() == 'en' else 'en'

    def get_to_main_btn_text(self) -> str:
        return 'На главную' if self.get_lang() == 'ru' else 'To main page'

    def get_to_game_btn_text(self) -> str:
        return 'На страницу игры' if self.get_lang() == 'ru' else 'To game page'

    def get_autho_btn_text(self) -> str:
        return 'Авторизация' if self.get_lang() == 'ru' else 'Authorization'

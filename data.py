import json
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/'
pages_path = path + 'static/pages/'
maps_path = path + 'static/maps/'
db_path = path + 'static/data/'

games_list = ('CS 2', 'Escape From Tarkov')  # список названий игр
games_short_names_list = ('cs2', 'eft')  # сокращённые названия игр (для ссылок)
maps_dict = {  # названия карт (доступ по [язык][игра][айди карты])
    'ru': {
        'cs2': ['', '', ''],
        'eft': ['', '', '']
    },
    'en': {
        'cs2': ['', '', ''],
        'eft': ['', '', '']
    }
}
games_dict = {'cs2': 'CS 2', 'eft': 'Escape From Tarkov'}  # названия по сокращению
games_with_spots = ('cs2', )  # список игр, где можно учить позиции
map_descriptions = {  # список файлов описания карт (доступ по [язык][игра][айди карты])
    'ru': {
        'cs2': ['', '', ''],
        'eft': ['', '', '']
    },
    'en': {
        'cs2': ['', '', ''],
        'eft': ['', '', '']
    }
}
now_in_moder_work = dict()


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


class SpotData:
    def __init__(self, db_name: str = db_path + 'add_spots.sqlite', save_mode: bool = False) -> None:
        if save_mode:
            # сохранить все данные от пользователя в бд
            pass
        else:
            self.ind = 0  # получить индекс ещё не обработанной заявки на добавление (использовать now_in_moder_work)
            # получить все данные

    def accept(self) -> None:
        # сохранить в бд
        pass

    def refuse(self) -> None:
        # eдалить запись из бд
        pass

    def sleep(self) -> None:
        # удалить из now_in_moder_work
        pass

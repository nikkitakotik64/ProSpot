import json
import os
import sqlite3

path = os.path.dirname(os.path.abspath(__file__)) + '/'
pages_path = path + 'static/pages/'
maps_path = path + 'static/maps/'
db_path = path + 'static/data/'
images_path = path + 'static/images/'
map_images_path = images_path + 'maps/'
game_images_path = images_path + 'games/'
spot_images_path = images_path + 'spots/'
memory_images_path = images_path + 'memory/'

games_list = ('CS 2', 'Escape From Tarkov')  # список названий игр
games_short_names_list = ('cs2', 'eft')  # сокращённые названия игр (для ссылок)
maps_dict = {  # названия карт (доступ по [язык][игра][айди карты])
    'ru': {
        'cs2': ['Mirage', 'Dust II', 'Anubis', 'Overpass', 'Inferno', 'Nuke', 'Ancient', 'Train', 'Vertigo',
                'Office', 'Italy'],
        'eft': ['Лаборатория', 'Эпицентр', 'Улицы Таркова', 'Развязка', 'Таможня', 'Завод', 'Лес', 'Резерв',
                'Маяк', 'Берег']
    },
    'en': {
        'cs2': ['Mirage', 'Dust II', 'Anubis', 'Overpass', 'Inferno', 'Nuke', 'Ancient', 'Train', 'Vertigo',
                'Office', 'Italy'],
        'eft': ['The Lab', 'Ground Zero', 'Streets of Tarkov', 'Interchange', 'Customs', 'Factory', 'Woods', 'Reserve',
                'Lighthouse', 'Shoreline']
    }
}
games_dict = {'cs2': 'CS 2', 'eft': 'Escape From Tarkov'}  # названия по сокращению
full_game_name = {'cs2': 'Counter-Strike 2', 'eft': 'Escape From Tarkov'}  # полные названия
games_short_name_dict = {'CS 2': 'cs2', 'Escape From Tarkov': 'eft'}  # сокращение по названию
games_with_spots = ('cs2', )  # список игр, где можно учить позиции
map_descriptions = {  # список файлов описания карт (доступ по [язык][игра][айди карты]), лежат в папке static/maps
    'ru': {
        'cs2': ['cs2_mirage_ru.txt', 'cs2_dust2_ru.txt', 'cs2_anubis_ru.txt', 'cs2_overpass_ru.txt',
                'cs2_inferno_ru.txt', 'cs2_nuke_ru.txt', 'cs2_ancient_ru.txt', 'cs2_train_ru.txt',
                'cs2_vertigo_ru.txt', 'cs2_office_ru.txt', 'cs2_italy_ru.txt'],
        'eft': ['', '', '']
    },
    'en': {
        'cs2': ['cs2_mirage_en.txt', 'cs2_dust2_en.txt', 'cs2_anubis_en.txt', 'cs2_overpass_en.txt',
                'cs2_inferno_en.txt', 'cs2_nuke_en.txt', 'cs2_ancient_en.txt', 'cs2_train_en.txt',
                'cs2_vertigo_en.txt', 'cs2_office_en.txt', 'cs2_italy_en.txt'],
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
        # удалить запись из бд
        pass

    def sleep(self) -> None:
        # удалить из now_in_moder_work
        pass


class MakeConnection:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.filename)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.connection.commit()
        self.connection.close()


class DBData:
    def __init__(self) -> None:
        self.db = db_path + 'spots.sqlite'
        self.connection_maker = MakeConnection(self.db)

    def save_added(self, game: str, map_name: str, pos: tuple[int, int] | None, name: str, filename: str) -> None:
        if pos is None:
            pos_x, pos_y = -1, -1
        else:
            pos_x, pos_y = pos
        with self.connection_maker as cur:
            try:
                ind = cur.execute('SELECT id FROM memory ORDER BY id').fetchall()[-1][0] + 1
            except IndexError:
                ind = 0
            cur.execute(f'INSERT INTO memory (id, map, pos_x, pos_y, name, image) '
                        f'VALUES ({ind}, "{map_name}", {pos_x}, {pos_y}, "{name}", "{filename}")')

    def generate_spot(self, game: str, map_name: str) -> int:
        # TODO
        return 1

    def get_spot(self, spot_id: int) -> tuple[str, int, int, str]:
        # TODO
        return 'Anubis', 190, 190, 'Connector'

    def get_accuracy(self, game: str, map_name: str, pos: tuple[int, int],
                     true_pos: tuple[int, int]) -> int:
        # TODO
        return 100


db_data = DBData()

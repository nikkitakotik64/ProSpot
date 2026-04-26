import json
import os
import sqlite3
import random
from PIL import Image

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
                'Office', 'Italy', 'Cache'],
        'eft': ['Лаборатория', 'Эпицентр', 'Улицы Таркова', 'Развязка', 'Таможня', 'Завод', 'Лес', 'Резерв',
                'Маяк', 'Берег']
    },
    'en': {
        'cs2': ['Mirage', 'Dust II', 'Anubis', 'Overpass', 'Inferno', 'Nuke', 'Ancient', 'Train', 'Vertigo',
                'Office', 'Italy', 'Cache'],
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
                'cs2_vertigo_ru.txt', 'cs2_office_ru.txt', 'cs2_italy_ru.txt', 'cs2_cache_ru.txt'],
        'eft': ['', '', '']
    },
    'en': {
        'cs2': ['cs2_mirage_en.txt', 'cs2_dust2_en.txt', 'cs2_anubis_en.txt', 'cs2_overpass_en.txt',
                'cs2_inferno_en.txt', 'cs2_nuke_en.txt', 'cs2_ancient_en.txt', 'cs2_train_en.txt',
                'cs2_vertigo_en.txt', 'cs2_office_en.txt', 'cs2_italy_en.txt', 'cs2_cache_en.txt'],
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
        game_name = full_game_name[games_short_name_dict[game]]
        if pos is None:
            pos_x, pos_y = -1, -1
        else:
            pos_x, pos_y = pos
        with self.connection_maker as cur:
            try:
                ind = cur.execute('SELECT id FROM memory ORDER BY id').fetchall()[-1][0] + 1
            except IndexError:
                ind = 0
            game_ind = cur.execute(f'SELECT id FROM games WHERE title = "{game_name}"').fetchone()[0]
            map_ind = cur.execute(f'SELECT id FROM maps WHERE title = "{map_name}" AND game = {game_ind}').fetchone()[0]
            cur.execute(f'INSERT INTO memory (id, map, pos_x, pos_y, name, image) '
                        f'VALUES ({ind}, "{map_ind}", {pos_x}, {pos_y}, "{name}", "{filename}")')

    def generate_spot(self, short_name: str, map_name: str) -> int:
        game_name = full_game_name[short_name]
        if map_name != 'Random' and map_name != 'Случайная':
            with self.connection_maker as cur:
                game_ind = cur.execute(f'SELECT id FROM games WHERE title = "{game_name}"').fetchone()[0]
                map_ind = cur.execute(f'SELECT id FROM maps WHERE title = "{map_name}" '
                                      f'AND game = {game_ind}').fetchone()[0]
                ids = cur.execute(f'SELECT id FROM spots WHERE map = {map_ind}').fetchall()
        else:
            with self.connection_maker as cur:
                game_ind = cur.execute(f'SELECT id FROM games WHERE title = "{game_name}"').fetchone()[0]
                ids = cur.execute(f'SELECT id FROM spots WHERE game = {game_ind}').fetchall()
        ids = list(map(lambda x: x[0], ids))
        return random.choice(ids)

    def get_spot(self, spot_id: int) -> tuple[str, int, int, str]:
        with self.connection_maker as cur:
            data = cur.execute(f'SELECT map, pos_x, pos_y, name FROM spots WHERE id = {spot_id}').fetchone()
            map_ind, pos_x, pos_y, name = data
            map_name = cur.execute(f'SELECT title FROM maps WHERE id = {map_ind}').fetchone()[0]
        return map_name, pos_x, pos_y, name

    def get_accuracy(self, short_name: str, map_name: str, pos: tuple[int, int],
                     true_pos: tuple[int, int]) -> int:
        pos = int(pos[0]), int(pos[1])
        true_pos = int(true_pos[0]), int(true_pos[1])
        rad = self.get_radius(short_name, map_name)
        dist = ((pos[0] - true_pos[0]) ** 2 + (pos[1] - true_pos[1]) ** 2) ** 0.5
        if dist < rad / 4:
            return 100
        dist -= rad / 4
        img = Image.open(map_images_path + self.get_map_image(short_name, map_name))
        size = min(img.size) / 2.8
        points = round(100 * (1 - dist / size) ** 2)
        if points == 100:
            points = 99
        if points < 0:
            points = 0
        return points

    def get_radius(self, short_name: str, map_name: str) -> int:
        img = Image.open(map_images_path + self.get_map_image(short_name, map_name))
        size = min(img.size)
        return round(size * 0.06)

    def get_spots(self, short_name: str, map_name: str) -> list[tuple[str, int, int]]:
        game_name = full_game_name[short_name]
        with self.connection_maker as cur:
            game_ind = cur.execute(f'SELECT id FROM games WHERE title = "{game_name}"').fetchone()[0]
            map_ind = cur.execute(f'SELECT id FROM maps WHERE title = "{map_name}" '
                                  f'AND game = {game_ind}').fetchone()[0]
            data = cur.execute(f'SELECT name, pos_x, pos_y FROM spots WHERE map = {map_ind}').fetchall()
        return data

    def get_images(self, short_name: str, map_name: str, spot: str) -> list[str]:
        game = full_game_name[short_name]
        images = []
        with self.connection_maker as cur:
            game_ind = cur.execute(f'SELECT id FROM games WHERE title = "{game}"').fetchone()[0]
            map_ind = cur.execute(f'SELECT id FROM maps WHERE title = "{map_name}" '
                                  f'AND game = {game_ind}').fetchone()[0]
            image = cur.execute(f'SELECT image FROM spots WHERE map = "{map_ind}" '
                                f'AND name = "{spot}"').fetchone()[0]
            images.append(image)
            try:
                image2 = cur.execute(f'SELECT image2 FROM spots WHERE map = "{map_ind}" '
                                     f'AND name = "{spot}"').fetchone()[0]
                if image2 is None:
                    raise TypeError
                images.append(image2)
                image3 = cur.execute(f'SELECT image3 FROM spots WHERE map = "{map_ind}" '
                                     f'AND name = "{spot}"').fetchone()[0]
                if image3 is None:
                    raise TypeError
                images.append(image3)
            except TypeError:
                pass
        return images

    def get_game_image(self, short_name: str) -> str:
        game = full_game_name[short_name]
        with self.connection_maker as cur:
            image = cur.execute(f'SELECT image FROM games WHERE title = "{game}"').fetchone()[0]
        return image

    def get_map_image(self, short_name: str, map_name: str) -> str:
        game = full_game_name[short_name]
        with self.connection_maker as cur:
            game_ind = cur.execute(f'SELECT id FROM games WHERE title = "{game}"').fetchone()[0]
            image = cur.execute(f'SELECT image FROM maps WHERE title = "{map_name}" '
                                f'AND game = {game_ind}').fetchone()[0]
        return image

    def get_spot_image(self, spot_id: int) -> str:
        with self.connection_maker as cur:
            image = cur.execute(f'SELECT image FROM spots WHERE id = {spot_id}').fetchone()[0]
        return image


db_data = DBData()  # глобальная константа для работы с бд

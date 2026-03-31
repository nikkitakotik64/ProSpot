import json
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/'
data_path = path + 'static/data/'

games_list = ('CS 2', 'Escape From Tarkov')


class Data:
    def __init__(self, text_filename: str) -> None:
        with open(text_filename, 'r', encoding='utf-8') as text_file:
            self.text_data = json.load(text_file)

    def get_phrase(self, key: str) -> str:
        return self.text_data[key]

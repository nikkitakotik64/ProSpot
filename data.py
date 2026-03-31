import json
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/'
data_path = path + 'static/data/'

games_list = ('CS 2', 'Escape From Tarkov')
langs = ['ru', 'en']


class Data:
    def __init__(self, text_filename: str) -> None:
        with open(text_filename, 'r', encoding='utf-8') as text_file:
            self.text_data = json.load(text_file)

    def get_phrase(self, key: str) -> str:
        return self.text_data[key]

    def get_lang(self) -> str:
        return self.text_data['lang']

    def get_another_langs(self) -> list[str]:
        ans = langs.copy()
        ans.remove(self.get_lang())
        return ans

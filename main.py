from pages import *
from flask import Flask
from data import Data, data_path

app = Flask(__name__)


@app.route('/')
@app.route('/ru')
@app.route('/main')
@app.route('/main/ru')
def return_main_page() -> str:
    data = Data(data_path + 'main_ru.json')
    return create_main_page(data)


@app.route('/en')
@app.route('/main/en')
def return_main_page_en() -> str:
    data = Data(data_path + 'main_en.json')
    return create_main_page(data)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

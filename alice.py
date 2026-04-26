from flask import Flask, request, jsonify
from data import (db_data, full_game_name, maps_dict, TextData,
                  pages_path, maps_path, map_descriptions)

app = Flask(__name__)


# Универсальные кнопки навигации
def get_nav_buttons(current_game=None):
    buttons = []
    if current_game:
        buttons.append({'title': 'К списку карт', 'hide': True})
    buttons.append({'title': 'К списку игр', 'hide': True})
    return buttons


@app.route('/post', methods=['POST'])
def main():
    data = request.json
    session_state = data.get('state', {}).get('session', {})
    response = {
        "version": data['version'],
        "session": data['session'],
        "response": {"end_session": False},
        "session_state": session_state
    }
    command = data['request']['command'].lower()

    # 1. Приветствие и Авторизация
    if data['session']['new']:
        response['response']['text'] = 'Добро пожаловать в ProSpot. Чтобы начать, авторизуйтесь.'
        response['response']['buttons'] = [{'title': 'Авторизация', 'hide': True}]
        return jsonify(response)

    if 'авторизация' in command:
        session_state['authorized'] = True
        response['response']['text'] = 'Вы авторизованы. Какую игру выберем?'
        response['response']['buttons'] = [{'title': 'Выбрать игру', 'hide': True}]
        return jsonify(response)

    if session_state.get('authorized'):

        # 2. Навигация: К списку игр
        if 'списку игр' in command or 'выбрать игру' in command:
            games_list = list(full_game_name.values())
            response['response']['text'] = 'Выберите игру из доступных:'
            response['response']['buttons'] = [{'title': g, 'hide': True} for g in games_list]
            return jsonify(response)

        # 3. Навигация: К списку карт
        current_game = session_state.get('current_game')
        if 'списку карт' in command and current_game:
            available_maps = maps_dict['ru'].get(current_game, [])
            response['response']['text'] = f'Карты игры {full_game_name[current_game]}:'
            buttons = [{'title': 'Получить информацию об игре', 'hide': True}]
            buttons.extend([{'title': m.capitalize(), 'hide': True} for m in available_maps])
            buttons.append({'title': 'К списку игр', 'hide': True})
            response['response']['buttons'] = buttons
            return jsonify(response)

        # 4. Обработка выбора ИГРЫ
        game_short_name = None
        for short, full in full_game_name.items():
            if full.lower() in command:
                game_short_name = short
                break

        if game_short_name:
            session_state['current_game'] = game_short_name
            available_maps = maps_dict['ru'].get(game_short_name, [])
            response['response']['text'] = f'Выбрана {full_game_name[game_short_name]}. Что показать?'
            buttons = [{'title': 'Получить информацию об игре', 'hide': True}]
            buttons.extend([{'title': m.capitalize(), 'hide': True} for m in available_maps])
            buttons.append({'title': 'К списку игр', 'hide': True})
            response['response']['buttons'] = buttons
            return jsonify(response)

        # 5. Инфо об игре
        if 'информацию об игре' in command and current_game:
            game_info_data = TextData(pages_path + current_game + '_info_ru.json')
            response['response']['text'] = game_info_data.get_phrase('text')
            response['response']['buttons'] = get_nav_buttons(current_game)
            return jsonify(response)

        # 6. Обработка выбора КАРТЫ
        if current_game:
            maps_list = maps_dict['ru'].get(current_game, [])
            for index, m_name in enumerate(maps_list):
                if m_name.lower() in command:
                    file_name = map_descriptions['ru'][current_game][index]
                    try:
                        with open(maps_path + file_name, 'r', encoding='utf-8') as f:
                            content = f.read()
                        response['response']['text'] = content
                    except:
                        response['response']['text'] = f'Описание карты {m_name} не найдено.'

                    response['response']['buttons'] = get_nav_buttons(current_game)
                    return jsonify(response)

    response['response']['text'] = 'Я вас не поняла. Воспользуйтесь кнопками навигации.'
    response['response']['buttons'] = get_nav_buttons(session_state.get('current_game'))
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

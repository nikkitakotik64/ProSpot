from data import TextData, pages_path, games_short_names_list, maps_dict, maps_path, map_descriptions
from flask_restful import Resource, reqparse
from data_db.db_functions import check_api_key


def get_game_info(lang, game):
    if game not in games_short_names_list:
        return None
    data = TextData(pages_path + game + f'_info_{lang}.json')
    return {"descriptions": data.get_phrase('text'), "maps": maps_dict[lang][game]}


def get_map_info(lang, game, map_name):
    if game not in games_short_names_list:
        return None
    if map_name not in maps_dict['en'][game]:
        return None
    map_id = maps_dict['en'][game].index(map_name)
    with open(maps_path + map_descriptions[lang][game][map_id]) as f:
        data = f.readlines()
        data = list(map(lambda x: x.rstrip(), data))
    return {"descriptions": data}


class SiteApi(Resource):
    @staticmethod
    def get():
        parser = reqparse.RequestParser()
        parser.add_argument('api_key', type=str, required=True)
        parser.add_argument('game', type=str, required=True)
        parser.add_argument('lang', type=str, default='en')
        parser.add_argument('map', type=str)
        args = parser.parse_args()
        map_name = args['map'].replace('_', ' ') if args['map'] else None
        data = None
        if args['lang'] not in ['ru', 'en']:
            return {"status": "error", "message": "Language not supported"}, 200
        if not check_api_key(args['api_key']):
            return {"status": "error", "message": "Invalid API key"}, 200
        if args['game']:
            if map_name:
                data = get_map_info(args['lang'], args['game'], map_name)
                if not data:
                    return {"status": "error", "message": "Map not found"}, 200
                return {"status": "success", "data": data}, 200
            data = get_game_info(args['lang'], args['game'])
            if not data:
                return {"status": "error", "message": "Game not found"}, 200
        if data:
            return {"status": "success", "data": data}, 200
        return {"status": "error", "message": "Not found"}, 200

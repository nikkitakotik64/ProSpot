from data import games_list, Data


def create_main_page(data: Data) -> str:
    page = f'''<!doctype html> 
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>ProSpot</title>
        </head>
        <body>
            <h0>{data.get_phrase('title')}</h0>
            <p>Тут должны быть кнопки игр</p>
            <p>{games_list}</p>
            <p>Тут должен быть визуальный разделитель</p>
            <p>Тут должна быть кнопка</p>
            <p>{data.get_phrase('add_spot_button')}</p>
            <p>Тут должен быть визуальный разделитель</p>
            <p>{data.get_phrase('tech_info')}</p>
        </body>
        </html>'''
    return page

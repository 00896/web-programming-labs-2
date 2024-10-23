from flask import Blueprint, url_for, redirect, render_template, request
lab2 = Blueprint('lab2',__name__)

@lab2.route('/lab2/a')
def a():
    return 'без слеша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слешем'


# flower_list = ['незабудка', 'одуванчик', 'колокольчик','гартензия']
# @lab2.route('/lab2/flowers/<int:flower_id>')
# def flowers(flower_id):
#     if flower_id >= len(flower_list):
#         return '''
#             <!doctype html>
#             <html>
#                 <body>
#                 <h1>Такого цветка нет</h1>
#                 <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
#                 </body>
#             </html>
#         ''', 404
#     else:
#         return f'''
#             <!doctype html>
#             <html>
#                 <body>
#                 <h1>Цветок: {flower_list[flower_id]}</h1>
#                 <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
#                 </body>
#             </html>
#         '''


# @lab2.route('/lab2/add_flower/', defaults={'name': None})
# @lab2.route('/lab2/add_flower/<name>')
# def add_flower(name):
#     if not name:
#          return "Вы не задали имя цветка", 400
#     flower_list.lab2end(name)
#     return f'''
# <!doctype html>
# <html>
#     <body>
#         <h1>Добавлен новый цветок</h1>
#         <p>Название нового цветка: {name}</p>
#         <p>Всего цветов: {len(flower_list)}</p>
#         <p>Полный список: {flower_list}</p>
#     </body>
# </html>
# '''


# @lab2.route('/lab2/flowers')
# def all_flowers():
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Все цветы</h1>
        <p>Количество цветов: {len(flower_list)}</p>
        <ul>
            {''.join([f'<li>{flower}</li>' for flower in flower_list])}
        </ul>
        <p><a href="/lab2/clear_flowers">Очистить список цветов</a></p>
    </body>
</html>
'''


@lab2.route('/lab2/example')
def example():
    name = 'Кобзева Лидия'
    number = '2'
    group = 'ФБИ-21'
    number_course = '3'
    fruits= [
        {'name':'груши', 'price':100},
        {'name':'апельсины', 'price':200},
        {'name':'бананы', 'price':150},
        {'name':'мандарины', 'price':180},
        {'name':'персики', 'price':250}
    ]
    return render_template('example.html', name=name, number=number, group=group, number_course=number_course, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных.."
    return render_template('filter.html', phrase=phrase)


@lab2.route('/lab2/calc/')
def default_calc():
    # Перенаправляем на /lab2/calc/1/1
    return redirect(url_for('lab2.calc', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def redirect_to_one(a):
    # Перенаправляем на /lab2/calc/a/1
    return redirect(url_for('lab2.calc', a=a, b=1))


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    # Выполняем математические операции
    results = {
        "sum": a + b,
        "difference": a - b,
        "product": a * b,
        "division": a / b if b != 0 else "деление на ноль",
        "power": a ** b
    }

    return f'''
        <!doctype html>
        <html>
            <head>
                <title>Результаты расчетов</title>
            </head>
            <body>
                <h1>Расчёт с параметрами:</h1>
                <ul>
                    <li>{a} + {b} = {results["sum"]}</li>
                    <li>{a} - {b} = {results["difference"]}</li>
                    <li>{a} x {b} = {results["product"]}</li>
                    <li>{a} / {b} = {results["division"]}</li>
                    <li>{a}^{b} = {results["power"]}</li>
                </ul>
                <p><a href="/lab2/calc">Вернуться к расчету</a></p>
            </body>
        </html>
    '''


books = [
    {"author": "Юваль Ной Харари", "title": "Sapiens. Краткая история человечества", "genre": "Научная литература", "pages": 512},
    {"author": "Стивен Кинг", "title": "Сияние", "genre": "Хоррор", "pages": 672},
    {"author": "Харуки Мураками", "title": "Норвежский лес", "genre": "Современная проза", "pages": 384},
    {"author": "Маргарет Этвуд", "title": "Рассказ служанки", "genre": "Антиутопия", "pages": 400},
    {"author": "Фрэнсис Скотт Фицджеральд", "title": "Великий Гэтсби", "genre": "Классическая литература", "pages": 180},
    {"author": "Александр Дюма", "title": "Граф Монте-Кристо", "genre": "Приключения", "pages": 1243},
    {"author": "Дуглас Адамс", "title": "Автостопом по галактике", "genre": "Научная фантастика", "pages": 224},
    {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 417},
    {"author": "Джордж Элиот", "title": "Мидлмарч", "genre": "Классическая литература", "pages": 880},
    {"author": "Умберто Эко", "title": "Имя розы", "genre": "Исторический детектив", "pages": 592}
]
@lab2.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)


parrot_breeds = [
    {
        "name": "Кубинский амазон",
        "image": "amazon.jpg",
        "description": "Населяет Кубу и прилегающие к ней острова: Багамские, Большой Кайман и Малый Кайман."
    },
    {
        "name": "Красный ара",
        "image": "ara.jpg",
        "description": "Крупный неотропический попугай желтого, красного и синего цветов, обитающий во влажных вечнозеленых лесах Америки."
    },
    {
        "name": "Какаду",
        "image": "kakadu.jpg",
        "description": "Ареал какаду ограничен Австралией, Новой Гвинеей и некоторыми островами Тихого океана."
    },
    {
        "name": "Жако",
        "image": "zako.jpg",
        "description": "Жако обитают в Западной и Центральной Африке."
    },
    {
        "name": "Лорикеты и какаду",
        "image": "loriket.jpg",
        "description": "Что-то обсуждают"
    },
    {
        "name": "Корелла и аратинга",
        "image": "korrel.jpg",
        "description": "Банный день луковицы"
    },
    {
        "name": "Неразлучники",
        "image": "family.jpg",
        "description": "Семейное фото"
    },
    {
        "name": "Сине-желтый ара",
        "image": "siniara.jpg",
        "description": "Ми тут проста созерцаем.."
    }
]
@lab2.route('/lab2/parrots')
def show_cats():
    return render_template('parrots.html', parrot_breeds=parrot_breeds)


flower_list = [
    {'name': 'незабудка', 'price': 100},
    {'name': 'одуванчик', 'price': 50},
    {'name': 'колокольчик', 'price': 150},
    {'name': 'гартензия', 'price': 300}
]

@lab2.route('/lab2/blossom/add', methods=['POST'])
def add_blossom():
    name = request.form.get('name')
    price = request.form.get('price')
    
    if not name or not price:
        return "Необходимо указать название и цену цветка", 400
    
    flower_list.append({'name': name, 'price': int(price)})
    return redirect(url_for('lab2.all_blossom'))


@lab2.route('/lab2/blossom')
def all_blossom():
    return render_template('blossom.html', flowers=flower_list)

@lab2.route('/lab2/blossom/delete/<int:flower_id>')
def delete_blossom(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        return "Цветок не найден", 404
    flower_list.pop(flower_id)
    return redirect(url_for('lab2.all_blossom'))

@lab2.route('/lab2/blossom/clear')
def clear_blossom():
    flower_list.clear()
    return redirect(url_for('lab2.all_blossom'))


from flask import Flask, url_for, redirect, render_template
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

@app.errorhandler(404)
def not_found():
    return "Нет такой страницы", 404


@app.route("/")
@app.route("/index")
def index():
    css = url_for("static", filename="main.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2</h1>
        </header>
        <ul>
        <li><a href="/lab1">Первая лабораторная</a></li>
        </ul>
        <ul>
        <li><a href="/lab2">Вторая лабораторная</a></li>
        </ul>
    <footer>
        <p>Кобзева Лидия Викторовна</p>
        <p>ФБИ-21, 3 курс, 2024 год</p>
    </footer>
    </body>
</html>
'''


@app.route('/400')
def bad_request():
    css = url_for("static", filename="main.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>Bad Request</title>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер обнаружил в запросе клиента синтаксическую ошибку</p>
    </body>
</html>
''', 400


@app.route('/401')
def unauthorized():
    css = url_for("static", filename="main.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>Unauthorized</title>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Для доступа к запрашиваемому ресурсу требуется аутентификация</p>
    </body>
</html>
''', 401


@app.route('/402')
def payment_required():
    css = url_for("static", filename="main.css")
    return '''
<!doctype html>
    <html>
    <head>
        <title>Payment Required</title>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>
            Этот код предусмотрен для платных пользовательских сервисов, и некорректно выдавать его 
            хостинг-провайдерам, если хозяин сайта не оплатил их услуги.
        </p>
    </body>
</html>
''', 402


@app.route('/403')
def forbidden():
    css = url_for("static", filename="main.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>Forbidden</title>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>
            Сервер понял запрос, но он отказывается его выполнять из-за ограничений в доступе 
            для клиента к указанному ресурсу
        </p>
    </body>
</html>
''', 403


@app.route('/404')
def still_not_found():
    css = url_for("static", filename="404.css")
    picture = url_for("static", filename="404.jpg")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css + '''">
        <title>Not Found</title>
    </head>
    <body>
        <h1 class='id'>404 Not Found</h1>
        <p>Ошибка в написании адреса Web-страницы</p>
        <img src="''' + picture + '''">
    </body>
</html>
''', 404


@app.route('/405')
def not_found():
    css = url_for("static", filename="main.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>Method Not Allowed</title>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Указанный клиентом метод нельзя применить к текущему ресурсу</p>
    </body>
</html>
''', 405


@app.route('/418')
def teapot():
    css = url_for("static", filename="main.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>I'm a teapot</title>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>
            Сервер не может приготовить кофе, потому что он чайник. Эта ошибка ссылается на Hyper Text Coffee Pot Control 
            Protocol (гипертекстовый протокол кофейников) который был первоапрельской шуткой в 1998 году
        </p>
    </body>
</html>
''', 418


# Обработчик, который будет вызывать ошибку на сервере и перехватчик
@app.route("/error")
def trigger_error():
    result = 8 / 0
    return f"Результат: {result}"


@app.errorhandler(500)
def internal_server_error(error):
    css = url_for("static", filename="main.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>Internal Server Error</title>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>500 Internal Server Error</h1>
        <p>Любая внутренняя ошибка сервера, которая не входит в рамки остальных ошибок класса</p>
    </body>
</html>
''', 500


@app.route('/lab2/a')
def a():
    return 'без слеша'

@app.route('/lab2/a/')
def a2():
    return 'со слешем'

flower_list = ['незабудка', 'одуванчик', 'колокольчик','гартензия']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return '''
            <!doctype html>
            <html>
                <body>
                <h1>Такого цветка нет</h1>
                <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
                </body>
            </html>
        ''', 404
    else:
        return f'''
            <!doctype html>
            <html>
                <body>
                <h1>Цветок: {flower_list[flower_id]}</h1>
                <p><a href="/lab2/flowers">Посмотреть все цветы</a></p>
                </body>
            </html>
        '''

@app.route('/lab2/add_flower/', defaults={'name': None})
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    if not name:
         return "Вы не задали имя цветка", 400
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/flowers')
def all_flowers():
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

@app.route('/lab2/example')
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

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных.."
    return render_template('filter.html', phrase=phrase)


@app.route('/lab2/calc/')
def default_calc():
    return redirect(url_for('calc', a=1, b=1)) #перенаправление на /lab2/calc/1/1

@app.route('/lab2/calc/<int:a>')
def redirect_to_oneurl(a):
    return redirect(url_for('calc', a=a, b=1)) #перенаправление на /lab2/calc/a/1

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
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
@app.route('/lab2/books')
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
@app.route('/lab2/parrots')
def show_cats():
    return render_template('parrots.html', parrot_breeds=parrot_breeds)
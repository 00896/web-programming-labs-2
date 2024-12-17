from flask import Flask, url_for, redirect, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

app = Flask(__name__)

import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретный ключ')
app.config['DB_TYPE'] = os.getenv ('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

#@app.errorhandler(404)
#def not_found():
#    return "Нет такой страницы", 404


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
            <li><a href="/lab2">Вторая лабораторная</a></li>
            <li><a href="/lab3/">Третья лабораторная</a></li>
            <li><a href="/lab4/">Четвертая лабораторная</a></li>
            <li><a href="/lab5/">Пятая лабораторная</a></li>
            <li><a href="/lab6/">Шестая лабораторная</a></li>
            <li><a href="/lab7/">Седьмая лабораторная</a></li>
            <li><a href="/lab8/">Восьмая лабораторная</a></li>
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

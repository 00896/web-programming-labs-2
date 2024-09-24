from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.errorhandler(404)
def not_found():
    return "Нет такой страницы", 404

@app.route("/lab1/web")
def web():
    return """<doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server':'sample',
            'Content-type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Кобзева Лидия Викторовна"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<doctype html>
        <html>
           <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/lab1/web">web</a>
           </body>
        </html>"""

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/oak")
def oak():
    path = url_for ("static", filename="cat.jpg")
    css = url_for("static", filename="lab1.css")
    return '''
<doctype html>
<html>
    <head>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>Дуб (почти дуб)</h1>
        <img src="'''+ path + '''">
    </body>
</html>'''

count = 0
@app.route("/lab1/counter")
def counter():
    global count 
    count += 1
    return '''
<doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <br>
        <a href="/lab1/reset_counter">Сбросить счетчик</a>
    </body>
</html>'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@app.route("/lab1/created")
def created():
    return '''
<doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div> 
    </body>
</html>
''', 201

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2</h1>
        </header>
        <ul>
        <li><a href="/lab1">Первая лабораторная</a></li>
        </ul>
    <footer>
        <p>Кобзева Лидия Викторовна</p>
        <p>ФБИ-21, 3 курс, 2024 год</p>
    </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
    <header>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2</h1>
    </header>

    <div>
        Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
    </div>
    <br>
    <div>
        <a href="/">На главную</a>
    </div>

    <footer>
        <p>Кобзева Лидия Викторовна</p>
        <p>ФБИ-21, 3 курс, 2024 год</p>
    </footer>
    </body>
</html>
'''

@app.route('/400')
def bad_request():
    return '''
<!doctype html>
<html>
    <head>
        <title>Bad Request</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер обнаружил в запросе клиента синтаксическую ошибку</p>
    </body>
</html>
''', 400

@app.route('/401')
def unauthorized():
    return '''
<!doctype html>
<html>
    <head>
        <title>Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Для доступа к запрашиваемому ресурсу требуется аутентификация</p>
    </body>
</html>
''', 401

@app.route('/402')
def payment_required():
    return '''
<!doctype html>
    <html>
    <head>
        <title>Payment Required</title>
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
    return '''
<!doctype html>
<html>
    <head>
        <title>Forbidden</title>
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

@app.route('/405')
def not_found():
    return '''
<!doctype html>
<html>
    <head>
        <title>Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Указанный клиентом метод нельзя применить к текущему ресурсу</p>
    </body>
</html>
''', 405

@app.route('/418')
def teapot():
    return '''
<!doctype html>
<html>
    <head>
        <title>I'm a teapot</title>
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
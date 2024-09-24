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
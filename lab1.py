from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1',__name__)

@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
def author():
    css = url_for("static", filename="main.css")
    name = "Кобзева Лидия Викторовна"
    group = "ФБИ-21"
    faculty = "ФБ"

    return '''<doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="'''+ css + '''">
            </head>
           <body>
               <p>Студент: ''' + name + '''</p>
               <p>Группа: ''' + group + '''</p>
               <p>Факультет: ''' + faculty + '''</p>
               <a href="/lab1/web">web</a>
           </body>
        </html>'''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/oak")
def oak():
    path = url_for ("static", filename="lab1/cat.jpg")
    css = url_for("static", filename="lab1/lab1.css")
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
@lab1.route("/lab1/counter")
def counter():
    css = url_for("static", filename="main.css")
    global count 
    count += 1
    return '''
<doctype html>
<html>
    <head>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <br></br>
        <a href="/lab1/reset_counter">Сбросить счетчик</a>
    </body>
</html>'''


@lab1.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")


resource_exists = False
@lab1.route("/lab1/created")
def created():
    css = url_for("static", filename="main.css")
    global resource_exists  # используем глобальную переменную для хранения состояния ресурса

    if resource_exists:
        return '''
<doctype html>
<html>
    <head>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>Отказано: ресурс уже создан</h1>
    </body>
</html>
''', 400
    else:
        resource_exists = True
        return '''
<doctype html>
<html>
    <head>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>Успешно: ресурс создан</h1>
        <div><i>Ресурс успешно создан.</i></div>
    </body>
</html>
''', 201


@lab1.route("/lab1/delete")
def delete():
    css = url_for("static", filename="main.css")
    global resource_exists

    if resource_exists:
        resource_exists = False
        return '''
<doctype html>
<html>
    <head>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>Успешно: ресурс удален</h1>
        <div><i>Ресурс успешно удален.</i></div>
    </body>
</html>
''', 200
    else:
        return '''
<doctype html>
<html>
    <head>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>Отказано: ресурс отсутствует</h1>
    </body>
</html>
''', 400


@lab1.route("/lab1/resource")
def resource():
    css = url_for("static", filename="main.css")
    global resource_exists

    if resource_exists:
        status = "Ресурс создан"
    else:
        status = "Ресурс ещё не создан"

    return '''
<doctype html>
<html>
    <head>
        <link rel="stylesheet" href="'''+ css + '''">
    </head>
    <body>
        <h1>Статус ресурса</h1>
        <div> '''+ status + '''</div>
        <br>
        <a href="/lab1/created">Создать ресурс</a>
        <br>
        <a href="/lab1/delete">Удалить ресурс</a>
    </body>
</html>
'''


@lab1.route("/lab1")
def lab():
    css = url_for("static", filename="main.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
        <link rel="stylesheet" href="'''+ css + '''">
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

    <h2>Список роутов:</h2>
    <ol>
        <li><a href="/lab1">Лабораторная 1</a></li>
        <li><a href="/lab1/web">Web-сервер на Flask</a></li>
        <li><a href="/lab1/author">Страница автора</a></li>
        <li><a href="/lab1/oak">Страница с дубом (почти)</a></li>
        <li><a href="/lab1/counter"> Счётчик посещений</a></li>
        <li><a href="/lab1/reset_counter">Сброс счётчика</a></li>
        <li><a href="/400">Код 400 </a></li>
        <li><a href="/401">Код 401 </a></li>
        <li><a href="/402">Код 402 </a></li>
        <li><a href="/403">Код 403 </a></li>
        <li><a href="/404">Код 404 </a></li>
        <li><a href="/405">Код 405 </a></li>
        <li><a href="/error">Код 500 </a></li>
        <li><a href="/kvezal">Квезаль </a></li>
        <li><a href="/lab1/resource">Статус ресурса</a></li>
    </ol>

    <footer>
        <p>Кобзева Лидия Викторовна</p>
        <p>ФБИ-21, 3 курс, 2024 год</p>
    </footer>
    </body>
</html>
'''


@lab1.route('/kvezal')
def kvezal():
    path = url_for("static", filename="lab1/kvezal.jpg")
    css_path = url_for("static", filename="lab1/kvezal.css")
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Квезаль</title>
            <link rel="stylesheet" href="''' + css_path + '''">
        </head>
        <body>
            <header>
                <h1>Аватар ацтекского Кетцалькоатля</h1>
            </header>
            <div>
                <div>
                    &nbsp; Это квезаль. Чудная птица из Центральной Америки. У неё невероятная внешность, яркая расцветка, 
                    а в полёте кудесница действительно напоминает что-то мифическое и волшебное. Квезаль подобен пернатому змею, 
                    грациозно рассекающему владения смертных.
                </div>
                <div>
                    <p>
                        &nbsp; Особенно забавно то, что ареал этих птиц полностью совпадает с бывшими владениями ацтекской империи. 
                        Считается, что носить длинные хвостовые перья квезалей было большой честью в обществе индейцев.
                        Птички исключительно мирные и кушают ягодки, иногда разбавляя насекомыми. Да и в целом, птица особо ничем 
                        не выделяется в образе жизни.
                    </p>
                    <p>
                        &nbsp; Но вид быстро вымирает. Браконьерство и вырубка лесов дают о себе знать. Ни одна программа по разведению этих 
                        птиц не увенчалась успехом: свободолюбивые боги не проживают и пары месяцев в неволе.
                    </p>
                </div>
            </div>
            <br>
            <img src="''' + path + '''" >
        </body>
    </html>
    ''', {
        'Kvezal':'Bird',
        'Page': 'Green'
    }
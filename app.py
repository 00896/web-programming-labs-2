from flask import Flask, url_for, redirect, render_template
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

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

resource_exists = False
@app.route("/lab1/created")
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

@app.route("/lab1/delete")
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

@app.route("/lab1/resource")
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
    <footer>
        <p>Кобзева Лидия Викторовна</p>
        <p>ФБИ-21, 3 курс, 2024 год</p>
    </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
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

@app.route('/kvezal')
def kvezal():
    path = url_for("static", filename="kvezal.jpg")
    css_path = url_for("static", filename="kvezal.css")
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
        return "Такого цветка нет", 404
    else:
        return "Цветок: " + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
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

@app.route('/lab2/example')
def example():
    name = 'Кобзева Лидия'
    number = '2'
    group = 'ФБИ-21'
    number_course = '3'
    return render_template('example.html', name=name, number=number, group=group, number_course=number_course)

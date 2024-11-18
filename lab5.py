from flask import Blueprint, session, redirect, render_template, request, url_for
lab5 = Blueprint('lab5',__name__)
import psycopg2
from psycopg2.extras import RealDictCursor

#пароль postgres dfgmoi45 lidia_kobzeva_knowledge_base

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))


@lab5.route('/lab5/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error = 'Заполните все поля')
    
    # для работы с БД нам нужно сначала подключиться к БД, затем получить курсор
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'lidia_kobzeva_knowledge_base',
        user = 'lidia_kobzeva_knowledge_base',
        password = 'dfgmoi45'
    )
    cur = conn.cursor()

    # далее сделаем SQL-запрос к БД, поищем пользователя с введённым логином
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    # fetchone() для получения результатов запроса
    if cur.fetchone():
        # перед тем, как выйти из обработчика по команде return, надо закрыть БД и курсор, иначе будут утечки памяти
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error = 'Такой пользователь уже существует')
    
    # если же пользователя в БД нет, то его можно зарегистрировать в системе, вставив в таблицу логин и пароль
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template ('lab5/success.html', login=login )


@lab5.route('/lab5/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error = 'Заполните все поля')
    
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'lidia_kobzeva_knowledge_base',
        user = 'lidia_kobzeva_knowledge_base',
        password = 'dfgmoi45'
    )
    cur = conn.cursor(cursor_factory= RealDictCursor)

    cur.execute(f"SELECT * FROM users WHERE login='{login}';")
    user = cur.fetchone()

    if not user:
        cur.close()
        conn.close()
        return render_template('lab5/login.html', error = 'Логин и/или пароль неверен')
    
    # если пользователь найден, то нужно прочитать его пароль — если введённый пароль не совпадает с паролем из БД, то выдать сообщение об ошибке
    if user['password'] !=password:
        cur.close()
        conn.close()
        return render_template('lab5/login.html', error = 'Логин и/или пароль неверен')
    
    session['login'] = login
    cur.close()
    conn.close()
    return render_template('lab5/success_login.html', login=login)
from flask import Blueprint, session, redirect, render_template, request, url_for
lab5 = Blueprint('lab5',__name__)
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

#пароль postgres dfgmoi45 lidia_kobzeva_knowledge_base

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    # для работы с БД нам нужно сначала подключиться к БД, затем получить курсор
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'lidia_kobzeva_knowledge_base',
        user = 'lidia_kobzeva_knowledge_base',
        password = 'dfgmoi45'
    )
    cur = conn.cursor(cursor_factory = RealDictCursor)

    return conn, cur

def db_close(conn,cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error = 'Заполните все поля')
    
    conn, cur = db_connect()

    # далее сделаем SQL-запрос к БД, поищем пользователя с введённым логином
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    # fetchone() для получения результатов запроса
    if cur.fetchone():
        # перед тем, как выйти из обработчика по команде return, надо закрыть БД и курсор, иначе будут утечки памяти
        db_close(conn,cur)
        return render_template('lab5/register.html', error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    # если же пользователя в БД нет, то его можно зарегистрировать в системе, вставив в таблицу логин и пароль
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password_hash}');")
    db_close(conn,cur)
    return render_template ('lab5/success.html', login=login )


@lab5.route('/lab5/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error = 'Заполните все поля')
    
    conn, cur = db_connect()

    cur.execute(f"SELECT * FROM users WHERE login='{login}';")
    user = cur.fetchone()

    if not user:
        db_close(conn,cur)
        return render_template('lab5/login.html', error = 'Логин и/или пароль неверен')
    
    # если пользователь найден, то нужно прочитать его пароль — если введённый пароль не совпадает с паролем из БД, то выдать сообщение об ошибке
    if not check_password_hash(user['password'], password):
        db_close(conn,cur)
        return render_template('lab5/login.html', error = 'Логин и/или пароль неверен')
    
    session['login'] = login
    db_close(conn,cur)
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods= ['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect ('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    conn,cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    login_id= cur.fetchone()["id"]

    cur.execute(f"INSERT INTO articles(login_id, title, article_text) \ 
                VALUES ({login_id},'{title}', '{article_text}');")
    
    db_close(conn, cur)
    return redirect('/lab5')
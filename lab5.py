from flask import Blueprint, session, redirect, render_template, request, current_app
lab5 = Blueprint('lab5',__name__)
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

#пароль postgres dfgmoi45 lidia_kobzeva_knowledge_base

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    # для работы с БД нам нужно сначала подключиться к БД, затем получить курсор
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'lidia_kobzeva_knowledge_base',
            user = 'lidia_kobzeva_knowledge_base',
            password = 'dfgmoi45'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

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
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))
    # fetchone() для получения результатов запроса
    if cur.fetchone():
        # перед тем, как выйти из обработчика по команде return, надо закрыть БД и курсор, иначе будут утечки памяти
        db_close(conn,cur)
        return render_template('lab5/register.html', error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    # если же пользователя в БД нет, то его можно зарегистрировать в системе, вставив в таблицу логин и пароль
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
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
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
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

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/')

@lab5.route('/lab5/create', methods= ['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect ('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        error_message = "Название статьи и текст не могут быть пустыми"
        return render_template('lab5/create_article.html', error_message=error_message)

    conn,cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))

    login_id= cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles(login_id, title, article_text) VALUES (%s, %s, %s);", (login_id, title, article_text))
    else:
        cur.execute("INSERT INTO articles(login_id, title, article_text) VALUES (?, ?, ?);", (login_id, title, article_text))

    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    conn, cur = db_connect()

    articles = []
    message = None

    if login:
        # Если пользователь авторизован, загружаем его статьи
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        login_id = cur.fetchone()["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "SELECT * FROM articles WHERE login_id=%s ORDER BY is_favorite DESC, id ASC;",
                (login_id,)
            )
        else:
            cur.execute(
                "SELECT * FROM articles WHERE login_id=? ORDER BY is_favorite DESC, id ASC;",
                (login_id,)
            )
        articles = cur.fetchall()

        if not articles:
            message = "У вас пока нет ни одной статьи"
    else:
        # Если пользователь не авторизован, показываем сообщение
        message = "Чтобы увидеть свои статьи, войдите"

    db_close(conn, cur)
    
    return render_template(
        '/lab5/articles.html',
        articles=articles,
        message=message,
        login=login
    )



@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
        article = cur.fetchone()

        if not article:
            db_close(conn, cur)
            return "Статья не найдена", 404

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        login_id = cur.fetchone()["id"]

        if article["login_id"] != login_id:
            db_close(conn, cur)
            return "Доступ запрещен", 403

        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        error_message = "Название статьи и текст не могут быть пустыми"
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article={"id": article_id, "title": title, "article_text": article_text}, error_message=error_message)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND login_id=%s;", (article_id, login_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND login_id=?;", (article_id, login_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена или доступ запрещен", 403

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/users')
def list_users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users;")
    else:
        cur.execute("SELECT login FROM users;")
    users = cur.fetchall()

    db_close(conn, cur)

    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/favorite/<int:article_id>', methods=['POST'])
def favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND login_id=%s;", (article_id, login_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND login_id=?;", (article_id, login_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена или доступ запрещен", 403

    new_status = not article["is_favorite"]
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s;", (new_status, article_id))
    else:
        cur.execute("UPDATE articles SET is_favorite=? WHERE id=?;", (new_status, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/public_articles')
def public_articles():
    conn, cur = db_connect()
    try:
        cur.execute("SELECT title, article_text, login_id FROM articles WHERE is_public = TRUE;")
        public_articles = cur.fetchall()
    finally:
        db_close(conn, cur)

    return render_template('/lab5/public_articles.html', articles=public_articles)
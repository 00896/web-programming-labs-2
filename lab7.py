from flask import Blueprint, session, redirect, render_template, request, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='lidia_kobzeva_knowledge_base',
            user='lidia_kobzeva_knowledge_base',
            password='dfgmoi45'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')

# Получение всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films")
    films = cur.fetchall()
    db_close(conn, cur)
    return films

# Получение одного фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if film:
        return film
    else:
        return {"error": "Film not found"}, 404

# Удаление фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = %s RETURNING id", (id,))
    deleted = cur.fetchone()
    db_close(conn, cur)
    if deleted:
        return '', 204
    else:
        return {"error": "Film not found"}, 404

# Обновление информации о фильме
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    if not film.get('description') or len(film['description']) > 2000:
        return {'description': 'Описание обязательно и должно содержать не более 2000 символов'}, 400
    if not film.get('title') and not film.get('title_ru'):
        return {'title': 'Укажите хотя бы одно название (оригинальное или русское)'}, 400
    if not film.get('title_ru'):
        return {'title_ru': 'Русское название обязательно'}, 400

    try:
        year = int(film.get('year', 0))
    except ValueError:
        return {'year': 'Год должен быть числом'}, 400
    current_year = 2024
    if not (1895 <= year <= current_year):
        return {'year': f'Год должен быть от 1895 до {current_year}'}, 400

    conn, cur = db_connect()
    cur.execute(
        """UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s RETURNING id""",
        (film['title'], film['title_ru'], film['year'], film['description'], id)
    )
    updated = cur.fetchone()
    db_close(conn, cur)
    if updated:
        return film
    else:
        return {"error": "Film not found"}, 404

# Добавление нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_films():
    film = request.get_json()
    if not film.get('description') or len(film['description']) > 2000:
        return {'description': 'Описание обязательно и должно содержать не более 2000 символов'}, 400
    if not film.get('title') and not film.get('title_ru'):
        return {'title': 'Укажите хотя бы одно название (оригинальное или русское)'}, 400
    if not film.get('title_ru'):
        return {'title_ru': 'Русское название обязательно'}, 400

    try:
        year = int(film.get('year', 0))
    except ValueError:
        return {'year': 'Год должен быть числом'}, 400
    current_year = 2024
    if not (1895 <= year <= current_year):
        return {'year': f'Год должен быть от 1895 до {current_year}'}, 400

    conn, cur = db_connect()
    cur.execute(
        "INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id",
        (film['title'], film['title_ru'], film['year'], film['description'])
    )
    new_id = cur.fetchone()["id"]
    db_close(conn, cur)
    return {"id": new_id}

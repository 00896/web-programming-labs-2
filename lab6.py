from flask import Blueprint, session, redirect, render_template, request, current_app
lab6 = Blueprint('lab6',__name__)
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor
from os import path

# для каждого офиса храниться информация: number —номер офиса,  
# tenant — арендатор. Если арендатор пуст, то это означает, что офис не арендуется
#offices = []
#for i in range(1,11):
#    offices.append({"number": i,"tenant": "", "price": 900 + i%9})


@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

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

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    login = session.get('login')
    
    conn, cur = db_connect()

    if data['method'] == 'info':
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
        offices = cur.fetchall()

        db_close(conn, cur)

        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    if data['method'] == 'calculate_cost':
        if not login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }
        
        # cуммируем стоимость аренды арендованных офисов
        cur.execute("""
            SELECT SUM(price) AS total_cost 
            FROM offices 
            WHERE tenant = %s
        """, (login,))
        result = cur.fetchone()

        total_cost = result['total_cost'] if result['total_cost'] else 0

        db_close(conn, cur)

        return {
            'jsonrpc': '2.0',
            'result': total_cost,
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        
        cur.execute("SELECT * FROM offices WHERE number = %s", (office_number,))
        office = cur.fetchone()
        
        if office and office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }

        if office:
            cur.execute("UPDATE offices SET tenant = %s WHERE number = %s", (login, office_number))
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': id
        }

    if data['method'] == 'cancellation':
        office_number = data['params']
        
        cur.execute("SELECT * FROM offices WHERE number = %s", (office_number,))
        office = cur.fetchone()
        
        if not office or not office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office is not rented'
                },
                'id': id
            }
        
        if office['tenant'] != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'You are not the tenant of this office'
                },
                'id': id
            }
        
        cur.execute("UPDATE offices SET tenant = NULL WHERE number = %s", (office_number,))
        db_close(conn, cur)
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    # если же метод нам неизвестен, вернём ошибку
    db_close(conn, cur)
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
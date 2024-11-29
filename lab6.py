from flask import Blueprint, session, redirect, render_template, request, current_app
lab6 = Blueprint('lab6',__name__)

# для каждого офиса храниться информация: number —номер офиса,  
# tenant — арендатор. Если арендатор пуст, то это означает, что офис не арендуется
offices = []
for i in range(1,11):
    offices.append({"number": i,"tenant": "", "price": 900 + i%9})


@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    login = session.get('login')

    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }    

    if data['method'] == 'calculate_cost':
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        total_cost = sum(office['price'] for office in offices if office['tenant'] == login)
        return {
            'jsonrpc': '2.0',
            'result': total_cost,
            'id': id
        }

    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }

                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if not office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not rented'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'You are not the tenant of this office'
                        },
                        'id': id
                    }

                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
           
    # если же метод нам неизвестен, вернём ошибку
    return{
        'jsonrpc':'2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
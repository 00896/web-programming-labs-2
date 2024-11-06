from flask import Blueprint, session, redirect, render_template, request, url_for
lab4 = Blueprint('lab4',__name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1') #данные получаются в строковом виде
    x2 = request.form.get('x2')
    if x1=='' or x2=='':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполненными!', error2 = 'На ноль делить нельзя!')

    x1 = int(x1) #преобразование данных из строк в числа
    x2 = int(x2)
    
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    #если какое-либо из полей пустое, то считать, что в него как будто бы ввели 0
    x1 = int(x1) if x1 else 0
    x2 = int(x2) if x2 else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/multiply-form')
def multiply_form():
    return render_template('lab4/multiply-form.html')


@lab4.route('/lab4/multiply', methods=['POST'])
def multiply():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    #если какое-либо из полей пустое, то считать, что в него как будто бы ввели 1
    x1 = int(x1) if x1 else 1
    x2 = int(x2) if x2 else 1
    
    result = x1 * x2
    return render_template('lab4/multiply.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    #выдавать ошибку при пустых полях
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполненными!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/expo-form')
def expo_form():
    return render_template('lab4/expo-form.html')


@lab4.route('/lab4/expo', methods=['POST'])
def expo():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    #выдавать ошибку при пустых полях, а также если оба поля равны нулю
    if x1 == '' or x2 == '':
        return render_template('lab4/expo.html', error='Оба поля должны быть заполненными!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/expo.html', error='0 в степени 0 не определено!')

    result = x1 ** x2
    return render_template('lab4/expo.html', x1=x1, x2=x2, result=result)


tree_count = 0
@lab4.route('/lab4/tree', methods=['POST','GET'])
def tree():
    global tree_count
    if request.method == 'GET': # значит, что на такую страницу пользователь просто вошёл
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')


    if operation == 'cut'and tree_count > 0:
        tree_count -=1
    elif operation == 'plant':
        tree_count += 1 

    return redirect ('/lab4/tree')


users = [
    {'login': 'alex', 'password': '1234', 'name': 'Alexander Ivanov', 'gender': 'male'},
    {'login':'bob','password':'555', 'name': 'Bob Ross', 'gender': 'male'},
    {'login':'oliver','password':'456', 'name': 'Olive Liviera', 'gender': 'male'},
    {'login':'tourist','password':'666', 'name': 'Турист', 'gender': 'male'}
]

@lab4.route('/lab4/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_login = session['login']
            user = next((u for u in users if u['login'] == user_login), None)
            name = user['name'] if user else user_login
        else: 
            authorized = False
            name = ''
        return render_template('lab4/login.html', authorized = authorized, name=name)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
    elif not password:
        error = 'Не введён пароль'
    else:
        user = next((u for u in users if u['login'] == login and u['password'] == password), None)
        if user:
            session['login'] = login
            return redirect('/lab4/login')
        error = 'Неверные логин и/или пароль'

    return render_template('lab4/login.html', error = error, authorized=False, login=login)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ""
    snowflakes = ""
    
    if request.method == 'POST':
        try:
            temperature = float(request.form.get('temperature'))
        except (TypeError, ValueError):
            message = "Ошибка: не задана температура"
            return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)

        if temperature < -12:
            message = "Не удалось установить температуру — слишком низкое значение"
        elif temperature > -1:
            message = "Не удалось установить температуру — слишком высокое значение"
        elif -12 <= temperature <= -9:
            message = f"Установлена температура: {temperature}°С"
            snowflakes = "❄️❄️❄️"  
        elif -8 <= temperature <= -5:
            message = f"Установлена температура: {temperature}°С"
            snowflakes = "❄️❄️"  
        elif -4 <= temperature <= -1:
            message = f"Установлена температура: {temperature}°С"
            snowflakes = "❄️"  

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)


grain_prices = {
    'Ячмень': 12345,
    'Овёс': 8522,
    'Пшеница': 8722,
    'Рожь': 14111
}

@lab4.route('/lab4/order_grain', methods=['GET', 'POST'])
def order_grain():
    if request.method == 'POST':
        grain = request.form.get('grain')
        try:
            weight = int(request.form.get('weight'))
            if weight <= 0:
                message = 'Ошибка: вес должен быть больше 0'
            elif weight > 500:
                message = 'Приносим извинения, такого объёма нет в наличии'
            else:
                price_per_ton = grain_prices[grain]
                total_price = price_per_ton * weight
                discount_applied = ''
                discount_amount = 0  #переменная для вывода суммы скидки
                if weight > 50:
                    discount_amount = total_price * 0.1 
                    total_price *= 0.9  
                    discount_applied = f' Применена скидка 10%, сумма скидки: {discount_amount:.2f} руб.'

                message = f'Заказ успешно сформирован. Вы заказали {grain}. Вес: {weight} т. Сумма к оплате: {total_price:.2f} руб.{discount_applied}'
            
            return redirect(url_for('lab4.order_grain', message=message))
        
        except (TypeError, ValueError):
            message = 'Ошибка: некорректно указан вес'
        except KeyError:
            message = 'Ошибка: не поддерживаемое зерно'
        
        return redirect(url_for('lab4.order_grain', message=message))
    
    message = request.args.get('message')
    return render_template('lab4/order_grain.html', message=message)
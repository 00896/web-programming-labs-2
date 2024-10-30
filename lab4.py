from flask import Blueprint, url_for, redirect, render_template, request
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


    if operation == 'cut':
        tree_count -=1
    elif operation == 'plant':
        tree_count += 1 

    return render_template('lab4/tree.html',tree_count=tree_count)
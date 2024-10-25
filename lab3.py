from flask import Blueprint, url_for, redirect, render_template, request, make_response
lab3 = Blueprint('lab3',__name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name','аноним')  #"аноним" по умол., пока name == None
    age = request.cookies.get('age', 'возраст неизвестен')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name','Alex', max_age=5)
    resp.set_cookie('age','20')
    resp.set_cookie('name_color','magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors={}
    user = request.args.get('user')
    if user == '':
        errors['user']= 'Заполните поле!'

    age = request.args.get('age','')
    if age == '':
        errors['age']= 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('/lab3/form1.html',user=user, age=age,sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 руб., черный чай - 80 руб, зеленый - 70 руб
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else: 
        price = 70

    #Добавка молока удорожает напиток на 30 руб, а сахара - на 10
    if request.args.get('milk')=='on':
        price += 30
    if request.args.get('sugar')=='on':
        price += 10
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background_color = request.args.get('background_color')
    font_size = request.args.get('font_size')
    font_weight = request.args.get('font_weight')  

    # если параметры переданы, устанавливаем их в куки
    if color or background_color or font_size or font_weight:
        resp = make_response(redirect('/lab3/settings'))

        if color:
            resp.set_cookie('color', color)  
        if background_color:
            resp.set_cookie('background_color', background_color) 
        if font_size:
            resp.set_cookie('font_size', font_size)  
        if font_weight:
            resp.set_cookie('font_weight', font_weight) 

        return resp  

    #в случае, если параметры не переданы, получаем их из куки
    color = request.cookies.get('color')
    background_color = request.cookies.get('background_color')
    font_size = request.cookies.get('font_size')
    font_weight = request.cookies.get('font_weight')  

    resp = make_response(render_template(
        'lab3/settings.html', 
        color=color, 
        background_color=background_color, 
        font_size=font_size,
        font_weight=font_weight  
    ))
    return resp 


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))

    resp.delete_cookie('color')
    resp.delete_cookie('background_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_weight')

    return resp


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        fcs = request.form.get('fcs')
        shelf = request.form.get('shelf')
        linen = request.form.get('linen') == 'on'
        baggage = request.form.get('baggage') == 'on'
        age = int(request.form.get('age', 0))
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        travel_date = request.form.get('travel_date')
        insurance = request.form.get('insurance') == 'on'

        if age < 1 or age > 120: #проверка возраста
            return "Ошибка: возраст должен быть от 1 до 120 лет.", 400

        # стоимость билета
        if age < 18:
            ticket_type = 'Детский билет'
            price = 700  
        else:
            ticket_type = 'Взрослый билет'
            price = 1000 

        # стоимость в зависимости от выбора полки
        if shelf in ['нижняя', 'нижняя боковая']:
            price += 100

        # увеличиваем стоимость за бельё
        if linen:
            price += 75

        # увеличиваем стоимость за багаж
        if baggage:
            price += 250

        # увеличиваем стоимость за страховку
        if insurance:
            price += 150

        return render_template('lab3/ticket.html', 
                               fcs=fcs, shelf=shelf, linen=linen, baggage=baggage, age=age, 
                               departure=departure, destination=destination, 
                               travel_date=travel_date, insurance=insurance, 
                               ticket_type=ticket_type, price=price)

    return render_template('lab3/formticket.html')


#доп.задание по списку ноутбуков
products = [
    {"name": "MacBook Air M1", "price": 999, "brand": "Apple", "color": "Silver"},
    {"name": "Dell XPS 13", "price": 1099, "brand": "Dell", "color": "Black"},
    {"name": "HP Spectre x360", "price": 1249, "brand": "HP", "color": "Silver"},
    {"name": "Asus ZenBook 14", "price": 899, "brand": "Asus", "color": "Blue"},
    {"name": "Lenovo ThinkPad X1 Carbon", "price": 1299, "brand": "Lenovo", "color": "Black"},
    {"name": "Acer Swift 3", "price": 699, "brand": "Acer", "color": "Gray"},
    {"name": "Microsoft Surface Laptop 4", "price": 1199, "brand": "Microsoft", "color": "Platinum"},
    {"name": "Razer Blade 15", "price": 1599, "brand": "Razer", "color": "Black"},
    {"name": "MSI GS66 Stealth", "price": 1799, "brand": "MSI", "color": "Black"},
    {"name": "Samsung Galaxy Book Pro", "price": 1049, "brand": "Samsung", "color": "Silver"},
    {"name": "Huawei MateBook X Pro", "price": 1399, "brand": "Huawei", "color": "Gray"},
    {"name": "LG Gram 17", "price": 1499, "brand": "LG", "color": "White"},
    {"name": "Google Pixelbook Go", "price": 849, "brand": "Google", "color": "Black"},
    {"name": "Asus ROG Zephyrus G14", "price": 1199, "brand": "Asus", "color": "White"},
    {"name": "Dell Inspiron 15", "price": 749, "brand": "Dell", "color": "Black"},
    {"name": "HP Pavilion 15", "price": 599, "brand": "HP", "color": "Silver"},
    {"name": "Lenovo Yoga 9i", "price": 1299, "brand": "Lenovo", "color": "Mica"},
    {"name": "Acer Predator Helios 300", "price": 1299, "brand": "Acer", "color": "Black"},
    {"name": "Microsoft Surface Pro 7", "price": 899, "brand": "Microsoft", "color": "Black"},
    {"name": "Razer Book 13", "price": 1399, "brand": "Razer", "color": "White"}
]
@lab3.route('/lab3/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
            # Получаем значения из формы
            try:
                min_price = int(request.form.get('min_price'))
                max_price = int(request.form.get('max_price'))
            except ValueError:
                return "Введите корректные числовые значения для цены."

            # Фильтруем товары по цене
            filtered_products = [
                product for product in products 
                if min_price <= product['price'] <= max_price
            ]

            # Передаем отфильтрованные товары в шаблон
            return render_template('lab3/search_results.html', products=filtered_products, min_price=min_price, max_price=max_price)

    return render_template('lab3/search_form.html')
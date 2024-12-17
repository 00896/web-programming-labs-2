from flask import Blueprint, session, redirect, render_template, request, current_app, url_for
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import NotFound

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register/', methods = ['GET', 'POST']) 
def register():
    if request.method =='GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login') 
    password_form = request.form.get('password')

    if not login_form or not login_form.strip():
        return render_template('lab8/register.html', error='Имя пользователя не может быть пустым')
    if not password_form or not password_form.strip():
        return render_template('lab8/register.html', error='Пароль не может быть пустым')

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return redirect('/lab8/')


@lab8.route('/lab8/login/', methods = ['GET', 'POST']) 
def login():
    if request.method =='GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login') 
    password_form = request.form.get('password')

    if not login_form or not login_form.strip():
        return render_template('lab8/login.html', error='Логин не может быть пустым')
    if not password_form or not password_form.strip():
        return render_template('lab8/login.html', error='Пароль не может быть пустым')

    user = users.query.filter_by(login = login_form).first()

    if user: 
        if check_password_hash(user.password, password_form):
            remember_me = request.form.get('remember') == 'on'
            login_user(user, remember=remember_me)
            return redirect('/lab8/')
        
    return render_template('/lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect ('/lab8/')


# Создание статьи
@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = True if request.form.get('is_favorite') else False
        is_public = True if request.form.get('is_public') else False
        
        if not title or not article_text:
            return render_template('lab8/create.html', error='Название и текст статьи обязательны для заполнения.')

        new_article = articles(
            login_id=current_user.id,
            title=title,
            article_text=article_text,
            is_favorite=is_favorite,
            is_public=is_public,
            likes=0
        )
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('lab8.article_list'))
    
    return render_template('lab8/create.html')


# Редактирование статьи
@lab8.route('/lab8/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get(article_id)
    
    if not article:
        raise NotFound("Статья не найдена.")
    
    # Проверка прав доступа
    if article.login_id != current_user.id:
        return redirect(url_for('lab8.article_list'))
    
    if request.method == 'POST':
        article.title = request.form.get('title')
        article.article_text = request.form.get('article_text')
        article.is_favorite = True if request.form.get('is_favorite') else False
        article.is_public = True if request.form.get('is_public') else False
        
        db.session.commit()
        return redirect(url_for('lab8.article_list'))

    return render_template('lab8/edit.html', article=article)


# Удаление статьи
@lab8.route('/lab8/delete/<int:article_id>/', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get(article_id)
    
    if not article:
        raise NotFound("Статья не найдена.")
    
    # Проверка прав доступа
    if article.login_id != current_user.id:
        return redirect(url_for('lab8.article_list'))

    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('lab8.article_list'))


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).order_by(articles.is_favorite.desc()).all()
    return render_template('lab8/articles.html', articles=user_articles)


# Публичные статьи - доступны всем пользователям
@lab8.route('/lab8/public_articles/')
def public_articles():
    query = request.args.get('q', '').strip()
    if query:
        public_articles = articles.query.filter(
            articles.is_public == True,  # Публичные статьи
            articles.title.ilike(f'%{query}%') | articles.article_text.ilike(f'%{query}%')
        ).all()
    else:
        public_articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=public_articles, query=query)


# Переключение любимой статьи
@lab8.route('/lab8/toggle_favorite/<int:article_id>/', methods=['POST'])
@login_required
def toggle_favorite(article_id):
    # Получаем статью по ID или возвращаем 404
    article = articles.query.get_or_404(article_id)

    # Проверяем, что текущий пользователь — автор статьи
    if article.login_id != current_user.id:
        return redirect(url_for('lab8.article_list'))

    # Переключаем статус "любимая" статьи
    article.is_favorite = not article.is_favorite
    db.session.commit()

    # Перенаправляем обратно на список статей
    return redirect(url_for('lab8.article_list'))
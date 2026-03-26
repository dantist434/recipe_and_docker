from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.database import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация пользователя"""
    if current_user.is_authenticated:
        return redirect(url_for('recipe.list_recipes'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Валидация
        if not all([username, email, password]):
            flash('Все поля обязательны для заполнения', 'danger')
        elif password != confirm_password:
            flash('Пароли не совпадают', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'danger')
        else:
            # Создание нового пользователя
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Авторизация пользователя"""
    if current_user.is_authenticated:
        return redirect(url_for('recipe.list_recipes'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('recipe.list_recipes'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))
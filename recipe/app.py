import os
from flask import Flask, render_template
from config import Config
from models.database import db
from flask_login import LoginManager
from models.user import User

# Инициализация Flask приложения
app = Flask(__name__,
            template_folder='views/templates',  # Указываем путь к шаблонам
            static_folder='views/static')  # Указываем путь к статике
app.config.from_object(Config)

# Инициализация базы данных
db.init_app(app)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Создание необходимых папок
def create_folders():
    """Создает необходимые папки для приложения"""
    folders = [
        'views/templates',
        'views/templates/auth',
        'views/templates/recipes',
        'views/templates/admin',
        'views/static/css',
        'views/static/js',
        'instance',
        'models',
        'controllers',
        'utils'
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)


# Регистрация Blueprints
from controllers.auth_controller import auth_bp
from controllers.recipe_controller import recipe_bp
from controllers.admin_controller import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(recipe_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


if __name__ == '__main__':
    create_folders()
    with app.app_context():
        # Создание таблиц в базе данных
        db.create_all()
    app.run(debug=True)
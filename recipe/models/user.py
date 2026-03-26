from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db


class User(UserMixin, db.Model):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin' или 'user'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Используем строку для ленивой загрузки, чтобы избежать циклической зависимости
    recipes = db.relationship('Recipe', backref='author', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Хэширование пароля"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверка пароля"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Проверка, является ли пользователь администратором"""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'
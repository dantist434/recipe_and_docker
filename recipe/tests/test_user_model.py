import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from models.database import db
from models.user import User
from models.recipe import Recipe


@pytest.fixture
def app():
    """Фикстура приложения Flask"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield app


class TestUserModel:
    """Тесты модели пользователя"""

    def test_user_creation(self, app):
        """1. Тест создания пользователя"""
        with app.app_context():
            user = User(username="test", email="test@example.com")
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

            fetched_user = User.query.filter_by(username="test").first()
            assert fetched_user.username == "test"
            assert fetched_user.email == "test@example.com"
            assert fetched_user.role == "user"  # По умолчанию

    def test_password_hashing(self, app):
        """2. Тест хэширования пароля"""
        with app.app_context():
            user = User(username="test", email="test@example.com")
            user.set_password("securepass")

            # Проверяем что пароль не хранится в открытом виде
            assert user.password_hash != "securepass"
            assert len(user.password_hash) > 10

    def test_password_check(self, app):
        """3. Тест проверки пароля"""
        with app.app_context():
            user = User(username="test", email="test@example.com")
            user.set_password("mypassword")

            assert user.check_password("mypassword") == True
            assert user.check_password("wrongpassword") == False

    def test_is_admin(self, app):
        """4. Тест проверки администратора"""
        with app.app_context():
            user = User(username="user", email="user@example.com")
            admin = User(username="admin", email="admin@example.com", role="admin")

            assert user.is_admin() == False
            assert admin.is_admin() == True

    def test_user_repr(self, app):
        """5. Тест строкового представления"""
        with app.app_context():
            user = User(username="testuser", email="test@example.com")

            assert repr(user) == "<User testuser>"
            assert "testuser" in str(user)
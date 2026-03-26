import pytest
from flask import Flask
from models.database import db
from models.user import User
from models.recipe import Recipe


@pytest.fixture
def app():
    """Фикстура приложения Flask для каждого теста"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield app

    # Очистка после теста
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_user(app):
    """Фикстура тестового пользователя"""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Получаем пользователя из базы чтобы он был привязан к сессии
        user = User.query.filter_by(username="testuser").first()
        return user


class TestRecipeModel:
    """Тесты модели рецепта"""

    def test_recipe_creation(self, app, test_user):
        """6. Тест создания рецепта"""
        with app.app_context():
            recipe = Recipe(
                title="Паста Карбонара",
                description="Вкусная паста",
                ingredients="Паста\nБекон\nЯйца\nСыр",
                instructions="Смешать все",
                cooking_time=20,
                difficulty="medium",
                category="Ужин",
                user_id=test_user.id
            )

            db.session.add(recipe)
            db.session.commit()

            fetched_recipe = Recipe.query.filter_by(title="Паста Карбонара").first()
            assert fetched_recipe.title == "Паста Карбонара"
            assert fetched_recipe.cooking_time == 20
            assert fetched_recipe.difficulty == "medium"
            assert fetched_recipe.user_id == test_user.id

    def test_ingredients_list(self, app, test_user):
        """7. Тест преобразования ингредиентов в список"""
        with app.app_context():
            recipe = Recipe(
                title="Тест",
                description="Тест",
                ingredients="Яйца 2 шт\nМука 100г\nСахар 50г",
                instructions="Смешать",
                cooking_time=10,
                difficulty="easy",
                category="Тест",
                user_id=test_user.id
            )

            ingredients = recipe.get_ingredients_list()
            assert isinstance(ingredients, list)
            assert len(ingredients) == 3
            assert ingredients[0] == "Яйца 2 шт"

    def test_instructions_list(self, app, test_user):
        """8. Тест преобразования инструкций в список"""
        with app.app_context():
            recipe = Recipe(
                title="Тест",
                description="Тест",
                ingredients="Ингредиенты",
                instructions="Шаг 1\nШаг 2\nШаг 3",
                cooking_time=10,
                difficulty="easy",
                category="Тест",
                user_id=test_user.id
            )

            # Не сохраняем в базу, просто тестируем метод
            instructions = recipe.get_instructions_list()
            assert isinstance(instructions, list)
            assert len(instructions) == 3
            assert instructions[2] == "Шаг 3"

    def test_empty_ingredients(self, app, test_user):
        """9. Тест пустых ингредиентов"""
        with app.app_context():
            recipe = Recipe(
                title="Тест",
                description="Тест",
                ingredients="",
                instructions="Инструкция",
                cooking_time=10,
                difficulty="easy",
                category="Тест",
                user_id=test_user.id
            )

            # Не сохраняем в базу, просто тестируем метод
            assert recipe.get_ingredients_list() == []

    def test_recipe_repr(self, app, test_user):
        """10. Тест строкового представления рецепта"""
        with app.app_context():
            recipe = Recipe(
                title="Моя паста",
                description="Тест",
                ingredients="Тест",
                instructions="Тест",
                cooking_time=10,
                difficulty="easy",
                category="Тест",
                user_id=test_user.id
            )

            # Не сохраняем в базу, просто тестируем метод
            assert repr(recipe) == "<Recipe Моя паста>"
            assert "Моя паста" in str(recipe)
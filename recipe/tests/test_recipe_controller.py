import pytest
from flask import Flask
from controllers.recipe_controller import recipe_bp


class TestRecipeController:
    """Тесты контроллера рецептов"""

    def test_recipe_blueprint_exists(self):
        """16. Тест существования Blueprint"""
        assert recipe_bp.name == "recipe"
        assert recipe_bp.url_prefix == "/recipes"

    def test_list_recipes_route(self):
        """17. Тест маршрута списка рецептов"""
        app = Flask(__name__)
        app.register_blueprint(recipe_bp)

        url_map = list(app.url_map.iter_rules())
        recipe_routes = [rule.endpoint for rule in url_map if rule.endpoint.startswith('recipe.')]

        assert 'recipe.list_recipes' in recipe_routes

    def test_create_recipe_route(self):
        """18. Тест маршрута создания рецепта"""
        app = Flask(__name__)
        app.register_blueprint(recipe_bp)

        url_map = list(app.url_map.iter_rules())
        recipe_routes = [rule.endpoint for rule in url_map if rule.endpoint.startswith('recipe.')]

        assert 'recipe.create_recipe' in recipe_routes

    def test_edit_recipe_route(self):
        """19. Тест маршрута редактирования рецепта"""
        app = Flask(__name__)
        app.register_blueprint(recipe_bp)

        url_map = list(app.url_map.iter_rules())
        recipe_routes = [rule.endpoint for rule in url_map if rule.endpoint.startswith('recipe.')]

        assert 'recipe.edit_recipe' in recipe_routes

    def test_delete_recipe_route(self):
        """20. Тест маршрута удаления рецепта"""
        app = Flask(__name__)
        app.register_blueprint(recipe_bp)

        url_map = list(app.url_map.iter_rules())
        recipe_routes = [rule.endpoint for rule in url_map if rule.endpoint.startswith('recipe.')]

        assert 'recipe.delete_recipe' in recipe_routes
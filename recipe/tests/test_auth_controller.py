import pytest
from flask import Flask
from controllers.auth_controller import auth_bp


class TestAuthController:
    """Тесты контроллера аутентификации"""

    def test_auth_blueprint_exists(self):
        """11. Тест существования Blueprint"""
        assert auth_bp.name == "auth"
        assert auth_bp.url_prefix == "/auth"

    def test_auth_routes_registered(self):
        """12. Тест регистрации маршрутов"""
        # Проверяем что Blueprint имеет правильные атрибуты
        assert hasattr(auth_bp, 'name')
        assert hasattr(auth_bp, 'url_prefix')
        assert auth_bp.name == 'auth'

    def test_login_route_exists(self):
        """13. Тест маршрута входа"""
        # Создаем тестовое приложение и регистрируем Blueprint
        app = Flask(__name__)
        app.register_blueprint(auth_bp)

        # Проверяем зарегистрированные маршруты
        url_map = list(app.url_map.iter_rules())
        auth_routes = [rule.endpoint for rule in url_map if rule.endpoint.startswith('auth.')]

        assert 'auth.login' in auth_routes

    def test_register_route_exists(self):
        """14. Тест маршрута регистрации"""
        app = Flask(__name__)
        app.register_blueprint(auth_bp)

        url_map = list(app.url_map.iter_rules())
        auth_routes = [rule.endpoint for rule in url_map if rule.endpoint.startswith('auth.')]

        assert 'auth.register' in auth_routes

    def test_logout_route_exists(self):
        """15. Тест маршрута выхода"""
        app = Flask(__name__)
        app.register_blueprint(auth_bp)

        url_map = list(app.url_map.iter_rules())
        auth_routes = [rule.endpoint for rule in url_map if rule.endpoint.startswith('auth.')]

        assert 'auth.logout' in auth_routes
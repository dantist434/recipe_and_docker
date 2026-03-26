import pytest
from flask import Flask
from controllers.admin_controller import admin_bp


class TestAdminController:
    """Тесты контроллера администратора"""

    def test_admin_blueprint_exists(self):
        """21. Тест существования Blueprint"""
        assert admin_bp.name == "admin"
        assert admin_bp.url_prefix == "/admin"

    def test_manage_users_route(self):
        """22. Тест маршрута управления пользователями"""
        app = Flask(__name__)
        app.register_blueprint(admin_bp)

        url_map = list(app.url_map.iter_rules())
        admin_routes = [rule.endpoint for rule in url_map if rule.endpoint.startswith('admin.')]

        assert 'admin.manage_users' in admin_routes

    def test_edit_user_route(self):
        """23. Тест маршрута редактирования пользователя"""
        app = Flask(__name__)
        app.register_blueprint(admin_bp)

        url_map = list(app.url_map.iter_rules())
        admin_routes = [rule.endpoint for rule in url_map if rule.endpoint.startswith('admin.')]

        assert 'admin.edit_user' in admin_routes
import pytest
from unittest.mock import Mock, patch
from flask import Flask, request, session
from flask_login import current_user
from utils.decorators import admin_required


class TestUtils:
    """Тесты утилит"""

    def test_decorator_creation(self):
        """24. Тест создания декоратора"""
        # Простая проверка что декоратор существует
        assert callable(admin_required)

        # Проверяем что это декоратор (возвращает функцию)
        def dummy_function():
            return "test"

        decorated = admin_required(dummy_function)
        assert callable(decorated)

    def test_decorator_returns_function(self):
        """25. Тест что декоратор возвращает функцию"""

        def test_func():
            return "original"

        decorated_func = admin_required(test_func)

        # Проверяем что возвращаемая функция может быть вызвана
        # (хотя и выдаст ошибку без контекста Flask)
        assert callable(decorated_func)
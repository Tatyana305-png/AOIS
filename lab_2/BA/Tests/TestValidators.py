import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Utils.Validators import ExpressionValidator


class TestValidators(BaseTestCase):
    """Тесты валидаторов"""

    def setUp(self):
        super().setUp()
        self.validator = ExpressionValidator()

    def test_validate_correct_expressions(self):
        """Тест валидации корректных выражений"""
        correct = [
            "a&b",
            "a|b",
            "!a",
            "a->b",
            "a~b",
            "(a&b)|c",
            "!(!a->!b)|c",
            "0",
            "1"
        ]

        for expr in correct:
            self.assertTrue(self.validator.validate(expr), f"Failed for {expr}")

    def test_validate_incorrect_expressions(self):
        """Тест валидации некорректных выражений"""
        incorrect = [
            "",  # пустое
            "a&",  # незаконченный оператор
            "a&x",  # недопустимая переменная
            "a&b)",  # лишняя скобка
            "(a&b",  # незакрытая скобка
            "&a",  # оператор в начале
            "a|",  # оператор в конце
        ]

        for expr in incorrect:
            self.assertFalse(self.validator.validate(expr), f"Should be invalid: {expr}")

    def test_check_characters(self):
        """Тест проверки символов"""
        self.assertTrue(self.validator.validate("a&b"))
        self.assertFalse(self.validator.validate("a&x"))

    def test_check_parentheses(self):
        """Тест проверки скобок"""
        self.assertTrue(self.validator.validate("(a&b)"))
        self.assertTrue(self.validator.validate("((a&b)|c)"))
        self.assertFalse(self.validator.validate("(a&b"))
        self.assertFalse(self.validator.validate("a&b)"))

    def test_check_operators(self):
        """Тест проверки операторов"""
        self.assertFalse(self.validator.validate("&a"))
        self.assertFalse(self.validator.validate("a|"))
        self.assertTrue(self.validator.validate("a&b"))
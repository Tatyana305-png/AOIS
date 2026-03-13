import re
from typing import List


class ExpressionValidator:
    """Валидатор логических выражений"""

    VALID_VARIABLES = {'a', 'b', 'c', 'd', 'e'}
    VALID_OPERATORS = {'&', '|', '!', '-', '>', '~', '(', ')'}

    @classmethod
    def validate(cls, expression: str) -> bool:
        """Проверка корректности выражения"""
        if not expression:
            return False

        # Удаляем пробелы
        expr = expression.replace(' ', '')

        # Проверка символов
        if not cls._check_characters(expr):
            return False

        # Проверка скобок
        if not cls._check_parentheses(expr):
            return False

        # Проверка операторов
        if not cls._check_operators(expr):
            return False

        return True

    @classmethod
    def _check_characters(cls, expr: str) -> bool:
        """Проверка допустимых символов"""
        i = 0
        while i < len(expr):
            char = expr[i]

            if char.isalpha():
                if char not in cls.VALID_VARIABLES:
                    return False
            elif char not in cls.VALID_OPERATORS and not char.isdigit():
                return False

            # Проверка составных операторов
            if char == '-' and i + 1 < len(expr) and expr[i + 1] == '>':
                i += 1  # пропускаем '>'

            i += 1

        return True

    @classmethod
    def _check_parentheses(cls, expr: str) -> bool:
        """Проверка баланса скобок"""
        balance = 0
        for char in expr:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    @classmethod
    def _check_operators(cls, expr: str) -> bool:
        """Проверка корректности использования операторов"""
        # Упрощенная проверка - можно расширить
        if expr.startswith(('&', '|', '~', '->')):
            return False
        if expr.endswith(('&', '|', '!', '-', '~')):
            return False
        return True
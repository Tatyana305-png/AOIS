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

        expr = expression.replace(' ', '')

        if not cls._check_characters(expr):
            return False

        if not cls._check_parentheses(expr):
            return False

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

            if char == '-' and i + 1 < len(expr) and expr[i + 1] == '>':
                i += 1

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
        if expr.startswith(('&', '|', '~', '->')):
            return False
        if expr.endswith(('&', '|', '!', '-', '~')):
            return False
        return True

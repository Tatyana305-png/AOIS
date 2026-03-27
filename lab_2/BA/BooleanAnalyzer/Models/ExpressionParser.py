import re
from typing import List, Dict
from abc import ABC, abstractmethod


class IExpressionParser(ABC):
    """Интерфейс для парсера выражений"""

    @abstractmethod
    def extract_variables(self, expression: str) -> List[str]:
        pass

    @abstractmethod
    def evaluate(self, expression: str, values: Dict[str, int]) -> int:
        pass

    @abstractmethod
    def validate_expression(self, expression: str) -> bool:
        pass


class BooleanExpressionParser(IExpressionParser):
    """Парсер булевых выражений"""

    SUPPORTED_OPERATIONS = {'&', '|', '!', '-', '~', '>', '(', ')', '='}
    VALID_VARIABLES = {'a', 'b', 'c', 'd', 'e'}
    VALID_CONSTANTS = {'0', '1'}

    def extract_variables(self, expression: str) -> List[str]:
        """Извлечение переменных из выражения"""
        var_pattern = r'[a-e]'
        vars_found = set(re.findall(var_pattern, expression))
        return sorted(list(vars_found))

    def evaluate(self, expression: str, values: Dict[str, int]) -> int:
        """Вычисление значения выражения"""
        expr = expression.replace(' ', '')

        if expr == '0':
            return 0
        if expr == '1':
            return 1

        for var, val in values.items():
            expr = expr.replace(var, str(val))

        expr = self._preprocess_expression(expr)

        try:
            result = eval(expr, {"__builtins__": {}}, {})
            return 1 if result else 0
        except Exception:
            return 0

    def validate_expression(self, expression: str) -> bool:
        """Проверка корректности выражения"""
        if not expression:
            return False

        expr = expression.replace(' ', '')

        if expr in ['0', '1']:
            return True

        if expr and expr[-1] in '&|!-~':
            return False

        if expr and expr[0] in '&|~':
            return False

        i = 0
        while i < len(expr):
            char = expr[i]

            if char == '-' and i + 1 < len(expr) and expr[i + 1] == '>':
                i += 1
            elif char == '!' and i + 1 < len(expr) and expr[i + 1] == '=':
                i += 1
            elif char.isalpha():
                if char not in self.VALID_VARIABLES:
                    return False
            elif char.isdigit():
                if char not in self.VALID_CONSTANTS:
                    return False
            elif char not in self.SUPPORTED_OPERATIONS:
                return False

            i += 1

        balance = 0
        for char in expr:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    return False

        return balance == 0

    def _preprocess_expression(self, expr: str) -> str:
        """Предобработка выражения"""

        expr = self._process_implication(expr)

        expr = expr.replace('~', ' == ')

        if '!=' in expr:
            parts = expr.split('!=')
            if len(parts) == 2:
                left = parts[0].strip()
                right = parts[1].strip()
                expr = f'(({left} and not {right}) or (not {left} and {right}))'

        expr = expr.replace('!', ' not ')
        expr = expr.replace('&', ' and ')
        expr = expr.replace('|', ' or ')

        return expr

    def _process_implication(self, expr: str) -> str:
        """Рекурсивная обработка импликации"""
        depth = 0
        for i in range(len(expr)):
            if expr[i] == '(':
                depth += 1
            elif expr[i] == ')':
                depth -= 1
            elif depth == 0 and i + 1 < len(expr) and expr[i] == '-' and expr[i + 1] == '>':
                left = expr[:i].strip()
                right = expr[i + 2:].strip()
                left = self._process_implication(left)
                right = self._process_implication(right)
                return f'(not ({left}) or ({right}))'

        return expr

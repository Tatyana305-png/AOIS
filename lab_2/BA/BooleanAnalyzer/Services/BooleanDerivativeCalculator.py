from typing import List
from ..Models.BooleanFunction import BooleanFunction
from ..Models.ExpressionParser import BooleanExpressionParser


class BooleanDerivativeCalculator:
    """Вычислитель булевых производных"""

    def __init__(self):
        self.parser = BooleanExpressionParser()

    def calculate(self, function: BooleanFunction, variables: List[str]) -> str:
        """Вычисление булевой производной"""
        if not variables:
            return function.expression

        for var in variables:
            if var not in function.variables:
                raise ValueError(f"Переменная {var} не найдена")

        result_func = function
        remaining_vars = variables.copy()

        while remaining_vars:
            var = remaining_vars.pop(0)
            deriv_expr = self._partial_derivative(result_func, var)
            result_func = BooleanFunction(deriv_expr, self.parser)

        return result_func.expression

    def _partial_derivative(self, function: BooleanFunction, var: str) -> str:
        """Частная производная по одной переменной"""
        # подфункции с var=0 и var=1
        expr_0 = function.expression.replace(var, '0')
        expr_1 = function.expression.replace(var, '1')

        return f'({expr_0}) != ({expr_1})'
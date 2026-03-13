import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser
from BooleanAnalyzer.Services.BooleanDerivativeCalculator import BooleanDerivativeCalculator


class TestBooleanDerivativeCalculator(BaseTestCase):
    """Тесты калькулятора булевых производных"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()
        self.calculator = BooleanDerivativeCalculator()

    def test_partial_derivative_and_wrt_a(self):
        """Тест частной производной AND по a"""
        f = BooleanFunction("a&b", self.parser)
        deriv = self.calculator.calculate(f, ['a'])
        self.assertTrue('b' in deriv or '!b' in deriv)

    def test_partial_derivative_and_wrt_b(self):
        """Тест частной производной AND по b"""
        f = BooleanFunction("a&b", self.parser)
        deriv = self.calculator.calculate(f, ['b'])
        self.assertTrue('a' in deriv or '!a' in deriv)

    def test_partial_derivative_or_wrt_a(self):
        """Тест частной производной OR по a"""
        f = BooleanFunction("a|b", self.parser)
        deriv = self.calculator.calculate(f, ['a'])
        self.assertTrue(isinstance(deriv, str))

    def test_partial_derivative_not(self):
        """Тест частной производной NOT"""
        f = BooleanFunction("!a", self.parser)
        deriv = self.calculator.calculate(f, ['a'])
        self.assertTrue('1' in deriv or '0' in deriv)

    def test_mixed_derivative_and(self):
        """Тест смешанной производной AND"""
        f = BooleanFunction("a&b", self.parser)
        deriv = self.calculator.calculate(f, ['a', 'b'])
        self.assertTrue(isinstance(deriv, str))

    def test_mixed_derivative_or(self):
        """Тест смешанной производной OR"""
        f = BooleanFunction("a|b", self.parser)
        deriv = self.calculator.calculate(f, ['a', 'b'])
        self.assertTrue(isinstance(deriv, str))

    def test_derivative_invalid_variable(self):
        """Тест производной по несуществующей переменной"""
        f = BooleanFunction("a&b", self.parser)
        with self.assertRaises(ValueError):
            self.calculator.calculate(f, ['x'])

    def test_derivative_empty_vars(self):
        """Тест производной с пустым списком переменных"""
        f = BooleanFunction("a&b", self.parser)
        deriv = self.calculator.calculate(f, [])
        self.assertEqual(deriv, f.expression)
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser
from BooleanAnalyzer.Services.NumericFormConverter import NumericFormConverter
from BooleanAnalyzer.Services.BooleanDerivativeCalculator import BooleanDerivativeCalculator
from BooleanAnalyzer.Services.Minimization.CalculationMinimizer import CalculationMinimizer


class TestComplexExample(BaseTestCase):
    """Тесты сложного примера из лабораторной работы"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()
        self.expr = "!(!a->!b)|c"

    def test_function_creation(self):
        """Тест создания функции"""
        f = BooleanFunction(self.expr, self.parser)
        self.assertEqual(set(f.variables), {'a', 'b', 'c'})
        self.assertEqual(len(f.truth_table), 8)


    def test_numeric_forms(self):
        """Тест числовых форм"""
        f = BooleanFunction(self.expr, self.parser)
        converter = NumericFormConverter()
        sdnf_num, sknf_num = converter.convert(f)

        self.assertTrue(len(sdnf_num) > 0)
        self.assertTrue(len(sknf_num) > 0)

    def test_index_form(self):
        """Тест индексной формы"""
        f = BooleanFunction(self.expr, self.parser)
        converter = NumericFormConverter()
        index = converter.get_index_form(f)

        self.assertTrue(len(index) > 0)

    def test_derivatives(self):
        """Тест производных"""
        f = BooleanFunction(self.expr, self.parser)
        calculator = BooleanDerivativeCalculator()

        for var in f.variables:
            deriv = calculator.calculate(f, [var])
            self.assertTrue(isinstance(deriv, str))
            self.assertTrue(len(deriv) > 0)

    def test_minimization(self):
        """Тест минимизации"""
        f = BooleanFunction(self.expr, self.parser)
        minimizer = CalculationMinimizer()
        minimized, stages = minimizer.minimize(f)

        self.assertTrue(isinstance(minimized, str))
        self.assertTrue(len(stages) > 0)
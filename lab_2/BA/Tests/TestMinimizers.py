from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser
from BooleanAnalyzer.Services.Minimization.CalculationMinimizer import CalculationMinimizer
from BooleanAnalyzer.Services.Minimization.TableCalculationMinimizer import TableCalculationMinimizer
from BooleanAnalyzer.Services.Minimization.KarnaughMinimizer import KarnaughMinimizer


class TestMinimizers(BaseTestCase):
    """Тесты минимизаторов"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()
        self.calc_minimizer = CalculationMinimizer()
        self.table_minimizer = TableCalculationMinimizer()
        self.karnaugh_minimizer = KarnaughMinimizer()

    def test_calculation_minimizer_simple(self):
        """Тест расчетного минимизатора для простой функции"""
        f = BooleanFunction("a&b|a&!b", self.parser)  # эквивалентно a
        minimized, stages = self.calc_minimizer.minimize(f)
        self.assertEqual(minimized, 'a')
        self.assertTrue(len(stages) > 0)

    def test_calculation_minimizer_identity(self):
        """Тест расчетного минимизатора для тождественной функции"""
        f = BooleanFunction("a", self.parser)
        minimized, stages = self.calc_minimizer.minimize(f)
        self.assertEqual(minimized, 'a')

    def test_calculation_minimizer_constant_0(self):
        """Тест расчетного минимизатора для константы 0"""
        f = BooleanFunction("a&!a", self.parser)
        minimized, stages = self.calc_minimizer.minimize(f)
        self.assertEqual(minimized, '0')

    def test_table_minimizer_simple(self):
        """Тест расчетно-табличного минимизатора"""
        f = BooleanFunction("a&b|a&!b", self.parser)
        minimized, stages, table = self.table_minimizer.minimize(f)
        self.assertEqual(minimized, 'a')
        self.assertTrue(table is not None)
        self.assertTrue('Импликанты' in table)

    def test_table_minimizer_complex(self):
        """Тест расчетно-табличного минимизатора для сложной функции"""
        f = BooleanFunction("!(!a->!b)|c", self.parser)
        minimized, stages, table = self.table_minimizer.minimize(f)
        self.assertTrue(isinstance(minimized, str))
        self.assertTrue(len(table) > 0)

    def test_karnaugh_minimizer_2var(self):
        """Тест минимизатора картой Карно для 2 переменных"""
        f = BooleanFunction("a&b", self.parser)
        minimized, k_map = self.karnaugh_minimizer.minimize(f)
        self.assertTrue('a&b' in minimized or 'b&a' in minimized)
        self.assertTrue(len(k_map) > 0)

    def test_karnaugh_minimizer_3var(self):
        """Тест минимизатора картой Карно для 3 переменных"""
        f = BooleanFunction("a&b&c", self.parser)
        minimized, k_map = self.karnaugh_minimizer.minimize(f)
        self.assertTrue('a&b&c' in minimized)

    def test_karnaugh_minimizer_4var(self):
        """Тест минимизатора картой Карно для 4 переменных"""
        f = BooleanFunction("a&b&c&d", self.parser)
        minimized, k_map = self.karnaugh_minimizer.minimize(f)
        self.assertTrue('a&b&c&d' in minimized)

    def test_karnaugh_minimizer_too_many_vars(self):
        """Тест минимизатора картой Карно с >4 переменными"""
        expr = "a&b&c&d&e"
        f = BooleanFunction(expr, self.parser)
        minimized, k_map = self.karnaugh_minimizer.minimize(f)
        self.assertTrue("до 4 переменных" in minimized)
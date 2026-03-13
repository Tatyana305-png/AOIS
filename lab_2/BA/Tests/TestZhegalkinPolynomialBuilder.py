import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser
from BooleanAnalyzer.Services.ZhegalkinPolynomialBuilder import ZhegalkinPolynomialBuilder


class TestZhegalkinPolynomialBuilder(BaseTestCase):
    """Тесты построителя полинома Жегалкина"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()
        self.builder = ZhegalkinPolynomialBuilder()

    def test_and_polynomial(self):
        """Тест полинома для AND"""
        f = BooleanFunction("a&b", self.parser)
        poly = self.builder.build(f)
        self.assertTrue('a&b' in poly or 'b&a' in poly)

    def test_or_polynomial(self):
        """Тест полинома для OR"""
        f = BooleanFunction("a|b", self.parser)
        poly = self.builder.build(f)
        terms = poly.split(' ⊕ ')
        self.assertEqual(len(terms), 3)

    def test_not_polynomial(self):
        """Тест полинома для NOT"""
        f = BooleanFunction("!a", self.parser)
        poly = self.builder.build(f)
        self.assertTrue('1' in poly or 'a' in poly)

    def test_equivalence_polynomial(self):
        """Тест полинома для эквивалентности"""
        f = BooleanFunction("a~b", self.parser)
        poly = self.builder.build(f)
        # a~b = 1 ⊕ a ⊕ b
        terms = poly.split(' ⊕ ')
        self.assertEqual(len(terms), 3)

    def test_constant_0_polynomial(self):
        """Тест полинома для константы 0"""
        f = BooleanFunction("0", self.parser)
        poly = self.builder.build(f)
        self.assertEqual(poly, '0')

    def test_constant_1_polynomial(self):
        """Тест полинома для константы 1"""
        f = BooleanFunction("1", self.parser)
        poly = self.builder.build(f)
        self.assertEqual(poly, '1')

    def test_complex_polynomial(self):
        """Тест полинома для сложной функции"""
        f = BooleanFunction("!(!a->!b)|c", self.parser)
        poly = self.builder.build(f)
        self.assertTrue(isinstance(poly, str))
        self.assertTrue(len(poly) > 0)
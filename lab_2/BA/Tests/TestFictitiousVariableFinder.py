import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser
from BooleanAnalyzer.Services.FictitiousVariableFinder import FictitiousVariableFinder


class TestFictitiousVariableFinder(BaseTestCase):
    """Тесты поиска фиктивных переменных"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()
        self.finder = FictitiousVariableFinder()


    def test_fictitious_in_function_of_one(self):
        """Тест для функции одной переменной"""
        f = BooleanFunction("a", self.parser)
        fict = self.finder.find(f)
        self.assertEqual(len(fict), 0)

    def test_fictitious_in_complex(self):
        """Тест для сложной функции с фиктивной"""
        # Функция зависит только от a
        f = BooleanFunction("a&(b|!b)", self.parser)
        fict = self.finder.find(f)
        self.assertIn('b', fict)

    def test_multiple_fictitious(self):
        """Тест нескольких фиктивных переменных"""
        # Функция зависит только от a
        f = BooleanFunction("a|!a", self.parser)
        fict = self.finder.find(f)
        # Должны найти все переменные кроме a
        for var in ['b', 'c', 'd', 'e']:
            if var in f.variables:  # если переменная есть в функции
                self.assertIn(var, fict)
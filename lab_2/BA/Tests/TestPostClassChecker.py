import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser
from BooleanAnalyzer.Services.PostClassChecker import PostClassChecker


class TestPostClassChecker(BaseTestCase):
    """Тесты проверки классов Поста"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()
        self.checker = PostClassChecker()

    def test_and_classes(self):
        """Тест классов для AND"""
        f = BooleanFunction("a&b", self.parser)
        classes = self.checker.check_all(f)

        self.assertTrue(classes['T0'])
        self.assertTrue(classes['T1'])
        self.assertFalse(classes['S'])
        self.assertTrue(classes['M'])

    def test_or_classes(self):
        """Тест классов для OR"""
        f = BooleanFunction("a|b", self.parser)
        classes = self.checker.check_all(f)

        self.assertTrue(classes['T0'])
        self.assertTrue(classes['T1'])
        self.assertFalse(classes['S'])
        self.assertTrue(classes['M'])

    def test_not_classes(self):
        """Тест классов для NOT"""
        f = BooleanFunction("!a", self.parser)
        classes = self.checker.check_all(f)

        self.assertFalse(classes['T0'])
        self.assertFalse(classes['T1'])
        self.assertTrue(classes['S'])
        self.assertFalse(classes['M'])

    def test_constant_0_classes(self):
        """Тест классов для константы 0"""
        f = BooleanFunction("0", self.parser)
        classes = self.checker.check_all(f)

        self.assertTrue(classes['T0'])
        self.assertFalse(classes['T1'])
        self.assertFalse(classes['S'])
        self.assertTrue(classes['M'])

    def test_constant_1_classes(self):
        """Тест классов для константы 1"""
        f = BooleanFunction("1", self.parser)
        classes = self.checker.check_all(f)

        self.assertFalse(classes['T0'])
        self.assertTrue(classes['T1'])
        self.assertFalse(classes['S'])
        self.assertTrue(classes['M'])

    def test_implication_classes(self):
        """Тест классов для импликации"""
        f = BooleanFunction("a->b", self.parser)
        classes = self.checker.check_all(f)

        self.assertFalse(classes['T0'])
        self.assertTrue(classes['T1'])
        self.assertFalse(classes['S'])
        self.assertFalse(classes['M'])
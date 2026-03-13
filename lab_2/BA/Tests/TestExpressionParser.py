import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser


class TestExpressionParser(BaseTestCase):
    """Тесты парсера выражений"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()

    def test_extract_variables_simple(self):
        """Тест извлечения переменных из простого выражения"""
        variables = self.parser.extract_variables("a&b")
        self.assertEqual(set(variables), {'a', 'b'})

    def test_extract_variables_complex(self):
        """Тест извлечения переменных из сложного выражения"""
        variables = self.parser.extract_variables("!a|b&c->d~e")
        self.assertEqual(set(variables), {'a', 'b', 'c', 'd', 'e'})

    def test_extract_variables_single(self):
        """Тест извлечения одной переменной"""
        variables = self.parser.extract_variables("!a")
        self.assertEqual(variables, ['a'])

    def test_evaluate_and_true(self):
        """Тест вычисления AND с истиной"""
        result = self.parser.evaluate("a&b", {'a': 1, 'b': 1})
        self.assertEqual(result, 1)

    def test_evaluate_and_false(self):
        """Тест вычисления AND с ложью"""
        result = self.parser.evaluate("a&b", {'a': 1, 'b': 0})
        self.assertEqual(result, 0)

    def test_evaluate_or_true(self):
        """Тест вычисления OR с истиной"""
        result = self.parser.evaluate("a|b", {'a': 0, 'b': 1})
        self.assertEqual(result, 1)

    def test_evaluate_or_false(self):
        """Тест вычисления OR с ложью"""
        result = self.parser.evaluate("a|b", {'a': 0, 'b': 0})
        self.assertEqual(result, 0)

    def test_evaluate_not(self):
        """Тест вычисления NOT"""
        result = self.parser.evaluate("!a", {'a': 1})
        self.assertEqual(result, 0)
        result = self.parser.evaluate("!a", {'a': 0})
        self.assertEqual(result, 1)

    def test_evaluate_implication_true(self):
        """Тест вычисления импликации с истиной"""
        result = self.parser.evaluate("a->b", {'a': 0, 'b': 0})
        self.assertEqual(result, 1)

    def test_evaluate_implication_false(self):
        """Тест вычисления импликации с ложью"""
        result = self.parser.evaluate("a->b", {'a': 1, 'b': 0})
        self.assertEqual(result, 0)

    def test_evaluate_equivalence_true(self):
        """Тест вычисления эквивалентности с истиной"""
        result = self.parser.evaluate("a~b", {'a': 0, 'b': 0})
        self.assertEqual(result, 1)

    def test_evaluate_equivalence_false(self):
        """Тест вычисления эквивалентности с ложью"""
        result = self.parser.evaluate("a~b", {'a': 0, 'b': 1})
        self.assertEqual(result, 0)

    def test_evaluate_xor(self):
        """Тест вычисления XOR"""
        result = self.parser.evaluate("a!=b", {'a': 0, 'b': 1})
        self.assertEqual(result, 1)
        result = self.parser.evaluate("a!=b", {'a': 1, 'b': 1})
        self.assertEqual(result, 0)

    def test_validate_correct_expression(self):
        """Тест валидации корректного выражения"""
        correct = [
            "a&b",
            "!a|(b&c)",
            "a->b",
            "(a~b)&c",
            "a!=b",
            "0",
            "1"
        ]
        for expr in correct:
            self.assertTrue(self.parser.validate_expression(expr), f"Failed for {expr}")

    def test_validate_incorrect_expression(self):
        """Тест валидации некорректного выражения"""
        incorrect = [
            "a&x",
            "a&b)",
            "(a&b",
            "",
        ]
        for expr in incorrect:
            self.assertFalse(self.parser.validate_expression(expr), f"Should be invalid: {expr}")
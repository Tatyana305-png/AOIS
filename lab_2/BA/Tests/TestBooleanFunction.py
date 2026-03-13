from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser


class TestBooleanFunction(BaseTestCase):
    """Тесты модели булевой функции"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()

    def test_creation_and(self):
        """Тест создания функции AND"""
        f = BooleanFunction("a&b", self.parser)
        self.assertEqual(set(f.variables), {'a', 'b'})
        self.assertEqual(len(f.truth_table), 4)

    def test_creation_or(self):
        """Тест создания функции OR"""
        f = BooleanFunction("a|b", self.parser)
        self.assertEqual(set(f.variables), {'a', 'b'})
        self.assertEqual(len(f.truth_table), 4)

    def test_creation_not(self):
        """Тест создания функции NOT"""
        f = BooleanFunction("!a", self.parser)
        self.assertEqual(f.variables, ['a'])
        self.assertEqual(len(f.truth_table), 2)

    def test_creation_complex(self):
        """Тест создания сложной функции"""
        f = BooleanFunction("!(!a->!b)|c", self.parser)
        self.assertEqual(set(f.variables), {'a', 'b', 'c'})
        self.assertEqual(len(f.truth_table), 8)

    def test_truth_table_and(self):
        """Тест таблицы истинности для AND"""
        f = BooleanFunction("a&b", self.parser)
        expected = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1}
        for bits, result in f.truth_table:
            self.assertEqual(result, expected[bits])

    def test_truth_table_or(self):
        """Тест таблицы истинности для OR"""
        f = BooleanFunction("a|b", self.parser)
        expected = {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1}
        for bits, result in f.truth_table:
            self.assertEqual(result, expected[bits])

    def test_truth_table_not(self):
        """Тест таблицы истинности для NOT"""
        f = BooleanFunction("!a", self.parser)
        expected = {(0,): 1, (1,): 0}
        for bits, result in f.truth_table:
            self.assertEqual(result, expected[bits])

    def test_truth_table_implication(self):
        """Тест таблицы истинности для импликации"""
        f = BooleanFunction("a->b", self.parser)
        expected = {(0, 0): 1, (0, 1): 1, (1, 0): 0, (1, 1): 1}
        for bits, result in f.truth_table:
            self.assertEqual(result, expected[bits])

    def test_truth_table_equivalence(self):
        """Тест таблицы истинности для эквивалентности"""
        f = BooleanFunction("a~b", self.parser)
        expected = {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 1}
        for bits, result in f.truth_table:
            self.assertEqual(result, expected[bits])

    def test_invalid_expression(self):
        """Тест создания с некорректным выражением"""
        with self.assertRaises(ValueError):
            BooleanFunction("a&", self.parser)

    def test_get_variable_count(self):
        """Тест получения количества переменных"""
        f = BooleanFunction("a&b", self.parser)
        self.assertEqual(f.get_variable_count(), 2)

        f = BooleanFunction("!a", self.parser)
        self.assertEqual(f.get_variable_count(), 1)

        f = BooleanFunction("a&b&c&d&e", self.parser)
        self.assertEqual(f.get_variable_count(), 5)

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        f = BooleanFunction("a&b", self.parser)
        data = f.to_dict()
        self.assertEqual(data['expression'], "a&b")
        self.assertEqual(set(data['variables']), {'a', 'b'})
        self.assertEqual(len(data['truth_table']), 4)
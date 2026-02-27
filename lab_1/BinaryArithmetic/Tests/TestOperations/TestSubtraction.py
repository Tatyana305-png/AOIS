import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Operations.Subtraction import Subtraction
from Operations.Addition import Addition


class TestSubtraction(unittest.TestCase):
    """Тесты для операции вычитания"""

    def setUp(self):
        self.subtraction = Subtraction(bits=8)

    def test_subtract_positive_positive(self):
        """Тест вычитания положительных чисел"""
        test_cases = [
            (10, 3, 7),
            (42, 15, 27),
            (50, 30, 20),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.subtraction.execute(a, b)
                self.assertEqual(result, expected)

    def test_subtract_positive_negative(self):
        """Тест вычитания отрицательного из положительного"""
        test_cases = [
            (10, -3, 13),
            (42, -15, 57),
            (50, -30, 80),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.subtraction.execute(a, b)
                self.assertEqual(result, expected)

    def test_subtract_negative_positive(self):
        """Тест вычитания положительного из отрицательного"""
        test_cases = [
            (-10, 3, -13),
            (-42, 15, -57),
            (-50, 30, -80),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.subtraction.execute(a, b)
                self.assertEqual(result, expected)

    def test_subtract_negative_negative(self):
        """Тест вычитания отрицательных чисел"""
        test_cases = [
            (-10, -3, -7),
            (-42, -15, -27),
            (-50, -30, -20),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.subtraction.execute(a, b)
                self.assertEqual(result, expected)

    def test_subtract_zero(self):
        """Тест вычитания нуля"""
        test_cases = [
            (5, 0, 5),
            (-5, 0, -5),
            (0, 5, -5),
            (0, -5, 5),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.subtraction.execute(a, b)
                self.assertEqual(result, expected)

    def test_subtract_identity(self):
        """Тест: A - A = 0"""
        numbers = [5, -5, 42, -42, 0]
        for num in numbers:
            with self.subTest(num=num):
                _, result = self.subtraction.execute(num, num)
                self.assertEqual(result, 0)

    def test_subtract_vs_addition(self):
        """Тест: A - B = A + (-B)"""

        addition = Addition(bits=8)
        test_cases = [(10, 3), (42, -15), (-10, -3), (0, 5)]

        for a, b in test_cases:
            with self.subTest(a=a, b=b):
                _, sub_result = self.subtraction.execute(a, b)
                _, add_result = addition.execute(a, -b)
                self.assertEqual(sub_result, add_result)


if __name__ == '__main__':
    unittest.main()
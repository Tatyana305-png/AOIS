import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Operations.Addition import Addition


class TestAddition(unittest.TestCase):
    """Тесты для операции сложения"""

    def setUp(self):
        self.addition = Addition(bits=8)

    def test_add_positive_positive(self):
        """Тест сложения двух положительных чисел"""
        test_cases = [
            (5, 3, 8),
            (42, 15, 57),
            (100, 27, 127),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.addition.execute(a, b)
                self.assertEqual(result, expected)

    def test_add_positive_negative(self):
        """Тест сложения положительного и отрицательного чисел"""
        test_cases = [
            (10, -5, 5),
            (42, -20, 22),
            (100, -50, 50),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.addition.execute(a, b)
                self.assertEqual(result, expected)

    def test_add_negative_negative(self):
        """Тест сложения двух отрицательных чисел"""
        test_cases = [
            (-5, -3, -8),
            (-42, -15, -57),
            (-100, -27, -127),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.addition.execute(a, b)
                self.assertEqual(result, expected)

    def test_add_zero(self):
        """Тест сложения с нулем"""
        test_cases = [
            (5, 0, 5),
            (-5, 0, -5),
            (0, 0, 0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.addition.execute(a, b)
                self.assertEqual(result, expected)

    def test_add_overflow(self):
        """Тест переполнения при сложении"""
        _, result = self.addition.execute(100, 50)
        self.assertEqual(result, -106)

    def test_add_underflow(self):
        """Тест отрицательного переполнения"""
        _, result = self.addition.execute(-100, -50)
        self.assertEqual(result, 106)

    def test_add_commutative(self):
        """Тест коммутативности сложения"""
        a, b = 15, -7
        _, result1 = self.addition.execute(a, b)
        _, result2 = self.addition.execute(b, a)
        self.assertEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()
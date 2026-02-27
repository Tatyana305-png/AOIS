import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Operations.Multiplication import Multiplication


class TestMultiplication(unittest.TestCase):
    """Тесты для операции умножения"""

    def setUp(self):
        self.multiplication = Multiplication(bits=8)

    def test_multiply_positive_positive(self):
        """Тест умножения положительных чисел"""
        test_cases = [
            (5, 3, 15),
            (12, 4, 48),
            (15, 7, 105),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.multiplication.execute(a, b)
                self.assertEqual(result, expected)

    def test_multiply_positive_negative(self):
        """Тест умножения положительного на отрицательное"""
        test_cases = [
            (5, -3, -15),
            (12, -4, -48),
            (15, -7, -105),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.multiplication.execute(a, b)
                self.assertEqual(result, expected)

    def test_multiply_negative_positive(self):
        """Тест умножения отрицательного на положительное"""
        test_cases = [
            (-5, 3, -15),
            (-12, 4, -48),
            (-15, 7, -105),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.multiplication.execute(a, b)
                self.assertEqual(result, expected)

    def test_multiply_negative_negative(self):
        """Тест умножения отрицательных чисел"""
        test_cases = [
            (-5, -3, 15),
            (-12, -4, 48),
            (-15, -7, 105),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.multiplication.execute(a, b)
                self.assertEqual(result, expected)

    def test_multiply_by_zero(self):
        """Тест умножения на ноль"""
        test_cases = [
            (5, 0, 0),
            (-5, 0, 0),
            (0, 5, 0),
            (0, -5, 0),
            (0, 0, 0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.multiplication.execute(a, b)
                self.assertEqual(result, expected)

    def test_multiply_by_one(self):
        """Тест умножения на единицу"""
        test_cases = [
            (5, 1, 5),
            (-5, 1, -5),
            (5, -1, -5),
            (-5, -1, 5),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.multiplication.execute(a, b)
                self.assertEqual(result, expected)

    def test_multiply_commutative(self):
        """Тест коммутативности умножения"""
        a, b = 7, -3
        _, result1 = self.multiplication.execute(a, b)
        _, result2 = self.multiplication.execute(b, a)
        self.assertEqual(result1, result2)

    def test_multiply_associative(self):
        """Тест ассоциативности умножения"""
        a, b, c = 3, 4, 5
        _, result1 = self.multiplication.execute(self.multiplication.execute(a, b)[1], c)
        _, result2 = self.multiplication.execute(a, self.multiplication.execute(b, c)[1])
        self.assertEqual(result1[1] if isinstance(result1, tuple) else result1,
                         result2[1] if isinstance(result2, tuple) else result2)


if __name__ == '__main__':
    unittest.main()
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Operations.Division import Division


class TestDivision(unittest.TestCase):
    """Тесты для операции деления"""

    def setUp(self):
        self.division = Division(bits=8, precision=5)

    def test_divide_positive_positive(self):
        """Тест деления положительных чисел"""
        test_cases = [
            (10, 2, 5.0),
            (15, 3, 5.0),
            (100, 4, 25.0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.division.execute(a, b)
                self.assertAlmostEqual(result, expected, places=5)

    def test_divide_positive_negative(self):
        """Тест деления положительного на отрицательное"""
        test_cases = [
            (10, -2, -5.0),
            (15, -3, -5.0),
            (100, -4, -25.0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.division.execute(a, b)
                self.assertAlmostEqual(result, expected, places=5)

    def test_divide_negative_positive(self):
        """Тест деления отрицательного на положительное"""
        test_cases = [
            (-10, 2, -5.0),
            (-15, 3, -5.0),
            (-100, 4, -25.0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.division.execute(a, b)
                self.assertAlmostEqual(result, expected, places=5)

    def test_divide_negative_negative(self):
        """Тест деления отрицательных чисел"""
        test_cases = [
            (-10, -2, 5.0),
            (-15, -3, 5.0),
            (-100, -4, 25.0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.division.execute(a, b)
                self.assertAlmostEqual(result, expected, places=5)

    def test_divide_with_precision(self):
        """Тест деления с точностью до 5 знаков"""
        test_cases = [
            (10, 3, 3.33333),
            (1, 3, 0.33333),
            (22, 7, 3.14285),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.division.execute(a, b)
                self.assertAlmostEqual(result, expected, places=4)

    def test_divide_by_one(self):
        """Тест деления на единицу"""
        test_cases = [
            (5, 1, 5.0),
            (-5, 1, -5.0),
            (5, -1, -5.0),
            (-5, -1, 5.0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.division.execute(a, b)
                self.assertAlmostEqual(result, expected, places=5)

    def test_divide_by_zero(self):
        """Тест деления на ноль (должно вызывать исключение)"""
        with self.assertRaises(ValueError):
            self.division.execute(5, 0)

    def test_divide_zero_by_number(self):
        """Тест деления нуля на число"""
        test_cases = [
            (0, 5, 0.0),
            (0, -5, 0.0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                _, result = self.division.execute(a, b)
                self.assertAlmostEqual(result, expected, places=5)


if __name__ == '__main__':
    unittest.main()
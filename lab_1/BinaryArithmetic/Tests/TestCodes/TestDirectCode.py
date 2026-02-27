import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Codes.DirectCode import DirectCode


class TestDirectCode(unittest.TestCase):
    """Тесты для прямого кода"""

    def setUp(self):
        self.code = DirectCode(bits=8)

    def test_direct_positive(self):
        """Тест прямого кода для положительных чисел"""
        test_cases = [
            (0, [0, 0, 0, 0, 0, 0, 0, 0]),
            (1, [0, 0, 0, 0, 0, 0, 0, 1]),
            (42, [0, 0, 1, 0, 1, 0, 1, 0]),
            (127, [0, 1, 1, 1, 1, 1, 1, 1]),
        ]

        for num, expected in test_cases:
            with self.subTest(num=num):
                result = self.code.to_binary(num)
                self.assertEqual(result, expected)

    def test_direct_negative(self):
        """Тест прямого кода для отрицательных чисел"""
        test_cases = [
            (-1, [1, 0, 0, 0, 0, 0, 0, 1]),
            (-42, [1, 0, 1, 0, 1, 0, 1, 0]),
            (-127, [1, 1, 1, 1, 1, 1, 1, 1]),
        ]

        for num, expected in test_cases:
            with self.subTest(num=num):
                result = self.code.to_binary(num)
                self.assertEqual(result, expected)

    def test_direct_from_binary_positive(self):
        """Тест преобразования из прямого кода (положительные)"""
        test_cases = [
            ([0, 0, 0, 0, 0, 0, 0, 0], 0),
            ([0, 0, 0, 0, 0, 0, 0, 1], 1),
            ([0, 0, 1, 0, 1, 0, 1, 0], 42),
        ]

        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.code.from_binary(bits)
                self.assertEqual(result, expected)

    def test_direct_from_binary_negative(self):
        """Тест преобразования из прямого кода (отрицательные)"""
        test_cases = [
            ([1, 0, 0, 0, 0, 0, 0, 1], -1),
            ([1, 0, 1, 0, 1, 0, 1, 0], -42),
            ([1, 1, 1, 1, 1, 1, 1, 1], -127),
        ]

        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.code.from_binary(bits)
                self.assertEqual(result, expected)

    def test_direct_roundtrip(self):
        """Тест полного цикла преобразования"""
        test_numbers = [0, 1, -1, 42, -42, 127, -127]
        for num in test_numbers:
            with self.subTest(num=num):
                binary = self.code.to_binary(num)
                result = self.code.from_binary(binary)
                self.assertEqual(result, num)


if __name__ == '__main__':
    unittest.main()
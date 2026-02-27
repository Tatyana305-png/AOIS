import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Codes.ReverseCode import ReverseCode


class TestReverseCode(unittest.TestCase):
    """Тесты для обратного кода"""

    def setUp(self):
        self.code = ReverseCode(bits=8)

    def test_reverse_positive(self):
        """Тест обратного кода для положительных чисел (должен совпадать с прямым)"""
        test_cases = [
            (0, [0, 0, 0, 0, 0, 0, 0, 0]),
            (1, [0, 0, 0, 0, 0, 0, 0, 1]),
            (42, [0, 0, 1, 0, 1, 0, 1, 0]),
        ]

        for num, expected in test_cases:
            with self.subTest(num=num):
                result = self.code.to_binary(num)
                self.assertEqual(result, expected)

    def test_reverse_negative(self):
        """Тест обратного кода для отрицательных чисел"""
        test_cases = [
            (-1, [1, 1, 1, 1, 1, 1, 1, 0]),
            (-42, [1, 1, 0, 1, 0, 1, 0, 1]),
            (-127, [1, 0, 0, 0, 0, 0, 0, 0]),
        ]

        for num, expected in test_cases:
            with self.subTest(num=num):
                result = self.code.to_binary(num)
                self.assertEqual(result, expected)

    def test_reverse_from_binary_positive(self):
        """Тест преобразования из обратного кода (положительные)"""
        test_cases = [
            ([0, 0, 0, 0, 0, 0, 0, 0], 0),
            ([0, 0, 0, 0, 0, 0, 0, 1], 1),
        ]

        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.code.from_binary(bits)
                self.assertEqual(result, expected)

    def test_reverse_from_binary_negative(self):
        """Тест преобразования из обратного кода (отрицательные)"""
        test_cases = [
            ([1, 1, 1, 1, 1, 1, 1, 0], -1),
            ([1, 1, 0, 1, 0, 1, 0, 1], -42),
        ]

        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.code.from_binary(bits)
                self.assertEqual(result, expected)

    def test_reverse_zero_negative(self):
        """Тест отрицательного нуля в обратном коде"""
        result = self.code.to_binary(-0)  # Должно работать как 0
        self.assertEqual(result, [0, 0, 0, 0, 0, 0, 0, 0])

    def test_reverse_roundtrip(self):
        """Тест полного цикла преобразования"""
        test_numbers = [0, 1, -1, 42, -42, 127, -127]
        for num in test_numbers:
            with self.subTest(num=num):
                binary = self.code.to_binary(num)
                result = self.code.from_binary(binary)
                self.assertEqual(result, num)


if __name__ == '__main__':
    unittest.main()
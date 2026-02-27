import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Codes.AdditionalCode import AdditionalCode


class TestAdditionalCode(unittest.TestCase):
    """Тесты для дополнительного кода"""

    def setUp(self):
        self.code = AdditionalCode(bits=8)

    def test_additional_positive(self):
        """Тест дополнительного кода для положительных чисел"""
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

    def test_additional_negative(self):
        """Тест дополнительного кода для отрицательных чисел"""
        test_cases = [
            (-1, [1, 1, 1, 1, 1, 1, 1, 1]),  # обратный код 11111110 + 1
            (-42, [1, 1, 0, 1, 0, 1, 1, 0]),  # обратный код 11010101 + 1
            (-127, [1, 0, 0, 0, 0, 0, 0, 1]),  # обратный код 10000000 + 1
            (-128, [1, 0, 0, 0, 0, 0, 0, 0]),  # минимальное значение
        ]

        for num, expected in test_cases:
            with self.subTest(num=num):
                result = self.code.to_binary(num)
                self.assertEqual(result, expected)

    def test_additional_from_binary_positive(self):
        """Тест преобразования из дополнительного кода (положительные)"""
        test_cases = [
            ([0, 0, 0, 0, 0, 0, 0, 0], 0),
            ([0, 0, 0, 0, 0, 0, 0, 1], 1),
            ([0, 0, 1, 0, 1, 0, 1, 0], 42),
        ]

        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.code.from_binary(bits)
                self.assertEqual(result, expected)

    def test_additional_from_binary_negative(self):
        """Тест преобразования из дополнительного кода (отрицательные)"""
        test_cases = [
            ([1, 1, 1, 1, 1, 1, 1, 1], -1),
            ([1, 1, 0, 1, 0, 1, 1, 0], -42),
            ([1, 0, 0, 0, 0, 0, 0, 1], -127),
            ([1, 0, 0, 0, 0, 0, 0, 0], -128),
        ]

        for bits, expected in test_cases:
            with self.subTest(bits=bits):
                result = self.code.from_binary(bits)
                self.assertEqual(result, expected)

    def test_additional_addition_property(self):
        """Тест свойства: A + (-A) = 0 в дополнительном коде"""
        numbers = [1, 42, 127]
        for num in numbers:
            with self.subTest(num=num):
                pos = self.code.to_binary(num)
                neg = self.code.to_binary(-num)

                # Складываем поразрядно
                result = []
                carry = 0
                for i in range(7, -1, -1):
                    total = pos[i] + neg[i] + carry
                    result.insert(0, total % 2)
                    carry = total // 2

                # Должен получиться 0 с переносом
                self.assertTrue(all(bit == 0 for bit in result))

    def test_additional_roundtrip(self):
        """Тест полного цикла преобразования"""
        test_numbers = [0, 1, -1, 42, -42, 127, -127, -128]
        for num in test_numbers:
            with self.subTest(num=num):
                binary = self.code.to_binary(num)
                result = self.code.from_binary(binary)
                self.assertEqual(result, num)


if __name__ == '__main__':
    unittest.main()
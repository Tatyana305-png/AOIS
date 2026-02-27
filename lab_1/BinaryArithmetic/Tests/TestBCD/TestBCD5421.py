import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from BCD.BCD5421 import BCD5421


class TestBCD5421(unittest.TestCase):
    """Тесты для 5421 BCD кода"""

    def setUp(self):
        self.bcd = BCD5421()

    def test_encode_single_digits(self):
        """Тест кодирования отдельных цифр"""
        test_cases = [
            (0, [0, 0, 0, 0]),
            (1, [0, 0, 0, 1]),
            (2, [0, 0, 1, 0]),
            (3, [0, 0, 1, 1]),
            (4, [0, 1, 0, 0]),
            (5, [1, 0, 0, 0]),
            (6, [1, 0, 0, 1]),
            (7, [1, 0, 1, 0]),
            (8, [1, 0, 1, 1]),
            (9, [1, 1, 0, 0]),
        ]

        for digit, expected in test_cases:
            with self.subTest(digit=digit):
                result = self.bcd.to_bcd(digit)
                # Для однозначных чисел первые 12 бит = 0
                self.assertEqual(result[0:12], [0] * 12)
                self.assertEqual(result[12:16], expected)

    def test_encode_two_digits(self):
        """Тест кодирования двузначных чисел"""
        test_cases = [
            (12, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]),
            (34, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0]),
            (56, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1]),
            (78, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1]),
            (90, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]),
        ]

        for num, expected in test_cases:
            with self.subTest(num=num):
                result = self.bcd.to_bcd(num)
                self.assertEqual(result, expected)


    def test_encode_four_digits(self):
        """Тест кодирования четырехзначных чисел"""
        test_cases = [
            (1234, [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0]),  # 1=тыс,2=сот,3=дес,4=ед
            (5678, [1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1]),  # 5=тыс,6=сот,7=дес,8=ед
            (9999, [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]),  # все 9
        ]

        for num, expected in test_cases:
            with self.subTest(num=num):
                result = self.bcd.to_bcd(num)
                self.assertEqual(result, expected)


    def test_encode_decode_roundtrip(self):
        """Тест полного цикла кодирования-декодирования"""
        test_numbers = [
            0, 1, 5, 7, 9,
            12, 34, 56, 78, 90,
            123, 456, 789, 999,
            1234, 5678, 9999
        ]

        for num in test_numbers:
            with self.subTest(num=num):
                encoded = self.bcd.to_bcd(num)
                decoded = self.bcd.from_bcd(encoded)
                self.assertEqual(decoded, num)

    def test_add_simple(self):
        """Тест сложения простых чисел"""
        test_cases = [
            (1, 2, 3),
            (5, 3, 8),
            (12, 34, 46),
            (123, 456, 579),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result_bcd, result = self.bcd.add(a, b)
                self.assertEqual(result, expected)
                decoded = self.bcd.from_bcd(result_bcd)
                self.assertEqual(decoded, expected)

    def test_add_with_carry(self):
        """Тест сложения с переносом"""
        test_cases = [
            (5, 5, 10),
            (9, 1, 10),
            (99, 1, 100),
            (555, 445, 1000),
            (4999, 5000, 9999),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result_bcd, result = self.bcd.add(a, b)
                self.assertEqual(result, expected)
                decoded = self.bcd.from_bcd(result_bcd)
                self.assertEqual(decoded, expected)

    def test_add_max_value(self):
        """Тест сложения с выходом за пределы"""
        with self.assertRaises(ValueError):
            self.bcd.add(9999, 1)

    def test_invalid_input(self):
        """Тест некорректного ввода"""
        with self.assertRaises(ValueError):
            self.bcd.to_bcd(-1)

        with self.assertRaises(ValueError):
            self.bcd.to_bcd(10000)

        with self.assertRaises(ValueError):
            self.bcd.from_bcd([0] * 15)


if __name__ == '__main__':
    unittest.main()
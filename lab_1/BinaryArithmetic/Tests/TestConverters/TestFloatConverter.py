import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Converters.FloatConverter import FloatConverter


class TestFloatConverter(unittest.TestCase):
    """Тесты для конвертера чисел с плавающей точкой IEEE-754"""

    def setUp(self):
        self.converter = FloatConverter()

    def test_float_to_binary_zero(self):
        """Тест преобразования нуля"""
        result = self.converter.to_binary(0.0)
        self.assertEqual(len(result), 32)
        self.assertTrue(all(bit == 0 for bit in result))

    def test_float_to_binary_one(self):
        """Тест преобразования единицы"""
        result = self.converter.to_binary(1.0)
        # 1.0 в IEEE-754: 0 01111111 00000000000000000000000
        self.assertEqual(result[0], 0)  # знак +
        self.assertEqual(result[1:9], [0, 1, 1, 1, 1, 1, 1, 1])
        self.assertTrue(all(bit == 0 for bit in result[9:]))

    def test_float_to_binary_negative_one(self):
        """Тест преобразования отрицательной единицы"""
        result = self.converter.to_binary(-1.0)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1:9], [0, 1, 1, 1, 1, 1, 1, 1])

    def test_float_to_binary_two(self):
        """Тест преобразования двойки"""
        result = self.converter.to_binary(2.0)
        # 2.0 = 1.0 * 2^1, экспонента = 128
        self.assertEqual(result[1:9], [1, 0, 0, 0, 0, 0, 0, 0])

    def test_float_to_binary_half(self):
        """Тест преобразования 0.5"""
        result = self.converter.to_binary(0.5)
        # 0.5 = 1.0 * 2^-1, экспонента = 126
        self.assertEqual(result[1:9], [0, 1, 1, 1, 1, 1, 1, 0])

    def test_binary_to_float(self):
        """Тест обратного преобразования"""
        test_numbers = [0.0, 1.0, -1.0, 2.0, 0.5, 12.5]
        for num in test_numbers:
            binary = self.converter.to_binary(num)
            result = self.converter.from_binary(binary)
            self.assertAlmostEqual(result, num, places=5)

    def test_float_12_5(self):
        """Тест для числа 12.5"""
        result = self.converter.to_binary(12.5)
        back = self.converter.from_binary(result)
        self.assertAlmostEqual(back, 12.5, places=5)

    def test_float_precision(self):
        """Тест точности представления"""
        num = 1.0 / 3.0
        binary = self.converter.to_binary(num)
        result = self.converter.from_binary(binary)
        self.assertLess(abs(result - num), 0.001)


if __name__ == '__main__':
    unittest.main()
import unittest
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Converters.BinaryConverter import BinaryConverter


class ConcreteConverter(BinaryConverter):
    """Конкретная реализация для тестирования"""

    def to_binary(self, number):
        return self._to_unsigned_binary(number)

    def from_binary(self, binary_array):
        return self._from_unsigned_binary(binary_array)


class TestBinaryConverter(unittest.TestCase):
    """Тесты для базового класса BinaryConverter"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.converter = ConcreteConverter(bits=8)

    def test_to_unsigned_binary_positive(self):
        """Тест преобразования положительного числа в беззнаковый двоичный код"""
        result = self.converter._to_unsigned_binary(42)
        expected = [0, 0, 1, 0, 1, 0, 1, 0]  # 42 в двоичной
        self.assertEqual(result, expected)

    def test_to_unsigned_binary_zero(self):
        """Тест преобразования нуля"""
        result = self.converter._to_unsigned_binary(0)
        expected = [0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(result, expected)

    def test_to_unsigned_binary_max(self):
        """Тест преобразования максимального значения для 8 бит"""
        result = self.converter._to_unsigned_binary(255)
        expected = [1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(result, expected)

    def test_to_unsigned_binary_negative(self):
        """Тест преобразования отрицательного числа"""
        result = self.converter._to_unsigned_binary(-1)
        # Для 8 бит -1 представляется как 255
        expected = [1, 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(result, expected)

    def test_from_unsigned_binary(self):
        """Тест преобразования из беззнакового двоичного кода"""
        bits = [0, 0, 1, 0, 1, 0, 1, 0]  # 42
        result = self.converter._from_unsigned_binary(bits)
        self.assertEqual(result, 42)

    def test_from_unsigned_binary_all_ones(self):
        """Тест преобразования всех единиц"""
        bits = [1, 1, 1, 1, 1, 1, 1, 1]
        result = self.converter._from_unsigned_binary(bits)
        self.assertEqual(result, 255)

    def test_from_unsigned_binary_all_zeros(self):
        """Тест преобразования всех нулей"""
        bits = [0, 0, 0, 0, 0, 0, 0, 0]
        result = self.converter._from_unsigned_binary(bits)
        self.assertEqual(result, 0)

    def test_different_bit_sizes(self):
        """Тест с разным количеством бит"""
        converter_16 = ConcreteConverter(bits=16)
        result = converter_16._to_unsigned_binary(42)
        self.assertEqual(len(result), 16)
        self.assertEqual(result[8:], [0, 0, 1, 0, 1, 0, 1, 0])
        self.assertTrue(all(bit == 0 for bit in result[:8]))


if __name__ == '__main__':
    unittest.main()
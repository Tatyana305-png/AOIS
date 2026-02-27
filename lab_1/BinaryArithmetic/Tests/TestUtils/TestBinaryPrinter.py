import unittest
import sys
import os
from io import StringIO
from contextlib import redirect_stdout

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Utils.BinaryPrinter import BinaryPrinter


class TestBinaryPrinter(unittest.TestCase):
    """Тесты для класса BinaryPrinter"""

    def setUp(self):
        self.printer = BinaryPrinter()
        self.output = StringIO()

    def test_print_binary_simple(self):
        """Тест вывода простого двоичного числа"""
        bits = [1, 0, 1, 0, 1, 0, 1, 0]

        with redirect_stdout(self.output):
            self.printer.print_binary(bits, "Тест")

        output = self.output.getvalue().strip()
        self.assertIn("Тест: 10101010", output)

    def test_print_binary_with_grouping(self):
        """Тест вывода с группировкой по умолчанию (8 бит)"""
        bits = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0]

        with redirect_stdout(self.output):
            self.printer.print_binary(bits)

        output = self.output.getvalue().strip()
        # Должно быть сгруппировано по 8 бит: 11110000 10101010
        self.assertIn("11110000 10101010", output)

    def test_print_binary_custom_grouping(self):
        """Тест вывода с пользовательской группировкой"""
        bits = [1, 1, 1, 1, 0, 0, 0, 0]

        with redirect_stdout(self.output):
            self.printer.print_binary(bits, group_size=4)

        output = self.output.getvalue().strip()
        self.assertIn("1111 0000", output)

    def test_print_section(self):
        """Тест вывода заголовка секции"""
        title = "ТЕСТОВАЯ СЕКЦИЯ"

        with redirect_stdout(self.output):
            self.printer.print_section(title)

        output = self.output.getvalue()
        self.assertIn("=" * 60, output)
        self.assertIn(title, output)

    def test_print_operation(self):
        """Тест вывода информации об операции"""
        bits = [1, 0, 1, 0, 1, 0, 1, 0]

        with redirect_stdout(self.output):
            self.printer.print_operation("Сложение", 5, 3, bits, 8)

        output = self.output.getvalue()
        self.assertIn("Сложение: 5 и 3", output)
        self.assertIn("Результат в двоичном виде: 10101010", output)
        self.assertIn("Результат в десятичном виде: 8", output)

    def test_print_number_conversion(self):
        """Тест вывода преобразования числа"""
        bits1 = [0, 0, 0, 0, 0, 0, 0, 1]
        bits2 = [0, 0, 0, 0, 0, 0, 0, 1]
        bits3 = [0, 0, 0, 0, 0, 0, 0, 1]

        with redirect_stdout(self.output):
            self.printer.print_number_conversion(1, bits1, bits2, bits3)

        output = self.output.getvalue()
        self.assertIn("Число: 1", output)
        self.assertIn("Прямой код: 00000001", output)

    def test_print_float_operation(self):
        """Тест вывода операции с плавающей точкой"""
        bits = [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]

        with redirect_stdout(self.output):
            self.printer.print_float_operation("1.0 + 2.0", 1.0, 2.0, bits, 3.0)

        output = self.output.getvalue()
        self.assertIn("1.0 + 2.0 (IEEE-754)", output)
        self.assertIn("Результат: 3.0", output)


if __name__ == '__main__':
    unittest.main()
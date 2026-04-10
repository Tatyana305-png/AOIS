import unittest
from bcd_summarizer import BCDSummarizer
from constants import BITS_IN_TETRAD, BCD_OFFSET


class TestBCDSummarizer(unittest.TestCase):
    """Тесты для BCD сумматора с оффсетом n=2"""

    def setUp(self):
        self.bcd = BCDSummarizer()

    def test_single_digit_addition(self):
        """Тест сложения однозначных BCD чисел С УЧЕТОМ оффсета n=2"""
        test_cases = [
            # (A, B, expected_tens, expected_units)
            ("0000", "0000", "0000", "0010"),  # 0+0+2=2
            ("0001", "0001", "0000", "0100"),  # 1+1+2=4
            ("0010", "0010", "0000", "0110"),  # 2+2+2=6
            ("0011", "0011", "0000", "1000"),  # 3+3+2=8
            ("0100", "0100", "0001", "0000"),  # 4+4+2=10
            ("0101", "0101", "0001", "0010"),  # 5+5+2=12
            ("0110", "0110", "0001", "0100"),  # 6+6+2=14
            ("0111", "0111", "0001", "0110"),  # 7+7+2=16
            ("1000", "1000", "0001", "1000"),  # 8+8+2=18
            ("1001", "1001", "0010", "0000"),  # 9+9+2=20
            ("1000", "0110", "0001", "0110"),  # 8+6+2=16
        ]

        for a, b, expected_tens, expected_units in test_cases:
            with self.subTest(a=a, b=b):
                self.bcd.execute(a, b)
                self.assertEqual(self.bcd.tens_digit, expected_tens)
                self.assertEqual(self.bcd.units_digit, expected_units)

    def test_get_full_result(self):
        """Тест форматирования полного результата"""
        self.bcd.execute("1000", "0110")
        self.assertEqual(self.bcd.get_full_result(), "0001 0110")  # 16

        self.bcd.execute("0000", "0000")
        self.assertEqual(self.bcd.get_full_result(), "0000 0010")  # 2

        self.bcd.execute("1001", "1001")
        self.assertEqual(self.bcd.get_full_result(), "0010 0000")  # 20

    def test_invalid_input_length(self):
        """Тест некорректной длины входных данных"""
        with self.assertRaises(ValueError):
            self.bcd.execute("111", "0000")

        with self.assertRaises(ValueError):
            self.bcd.execute("0000", "11111")

    def test_invalid_input_characters(self):
        """Тест некорректных символов во входных данных"""
        with self.assertRaises(ValueError):
            self.bcd.execute("1002", "0000")

        with self.assertRaises(ValueError):
            self.bcd.execute("1A00", "0110")

    def test_offset_constant(self):
        """Проверка значения оффсета"""
        self.assertEqual(BCD_OFFSET, 2)


if __name__ == "__main__":
    unittest.main()
import unittest
from parallel_adder import ParallelAdder


class TestParallelAdder(unittest.TestCase):
    """Тесты для 4-битного параллельного сумматора"""

    def setUp(self):
        self.adder = ParallelAdder()

    def test_addition_without_carry(self):
        """Тест сложения без входного переноса"""
        test_cases = [
            ("0000", "0000", "0000", 0),
            ("0001", "0001", "0010", 0),
            ("0010", "0011", "0101", 0),
            ("0101", "0010", "0111", 0),
            ("0111", "0001", "1000", 0),
            ("1111", "0000", "1111", 0),
            ("1010", "0101", "1111", 0),
            ("1000", "0110", "1110", 0),
        ]

        for a, b, expected_sum, expected_carry in test_cases:
            with self.subTest(a=a, b=b):
                self.adder.process_addition(a, b, False)
                self.assertEqual(self.adder.get_result_string(), expected_sum)
                self.assertEqual(self.adder.get_final_carry(), bool(expected_carry))

    def test_addition_with_carry(self):
        """Тест сложения с входным переносом"""
        test_cases = [
            ("0000", "0000", "0001", 0),
            ("0001", "0001", "0011", 0),
            ("0111", "0001", "1001", 0),
            ("1111", "0000", "0000", 1),
            ("1111", "0001", "0001", 1),
            ("1000", "0111", "0000", 1),
            ("1000", "0110", "1111", 0),
        ]

        for a, b, expected_sum, expected_carry in test_cases:
            with self.subTest(a=a, b=b):
                self.adder.process_addition(a, b, True)
                self.assertEqual(self.adder.get_result_string(), expected_sum)
                self.assertEqual(self.adder.get_final_carry(), bool(expected_carry))

    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Максимальное значение
        self.adder.process_addition("1111", "1111", False)
        self.assertEqual(self.adder.get_result_string(), "1110")
        self.assertEqual(self.adder.get_final_carry(), True)

        # Максимальное значение с переносом
        self.adder.process_addition("1111", "1111", True)
        self.assertEqual(self.adder.get_result_string(), "1111")
        self.assertEqual(self.adder.get_final_carry(), True)

        # Нулевые значения
        self.adder.process_addition("0000", "0000", False)
        self.assertEqual(self.adder.get_result_string(), "0000")
        self.assertEqual(self.adder.get_final_carry(), False)

    def test_invalid_input_length(self):
        """Тест некорректной длины входных данных"""
        with self.assertRaises(ValueError):
            self.adder.process_addition("111", "0000", False)

        with self.assertRaises(ValueError):
            self.adder.process_addition("0000", "11111", False)

    def test_invalid_input_characters(self):
        """Тест некорректных символов во входных данных"""
        with self.assertRaises(ValueError):
            self.adder.process_addition("1002", "0000", False)

        with self.assertRaises(ValueError):
            self.adder.process_addition("1A00", "0110", False)


if __name__ == "__main__":
    unittest.main()
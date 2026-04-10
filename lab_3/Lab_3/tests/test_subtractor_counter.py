import unittest
from subtractor_counter import SubtractorCounter
from constants import BITS_IN_3BIT_COUNTER, COUNTER_MAX_VALUE


class TestSubtractorCounter(unittest.TestCase):
    """Тесты для программного вычитающего счетчика"""

    def test_initialization_valid(self):
        """Тест инициализации с корректным значением"""
        for i in range(COUNTER_MAX_VALUE + 1):
            with self.subTest(start_value=i):
                counter = SubtractorCounter(i)
                self.assertEqual(counter.get_current_value_decimal(), i)
                self.assertEqual(counter.get_current_value_binary(), format(i, f"0{BITS_IN_3BIT_COUNTER}b"))

    def test_initialization_invalid(self):
        """Тест инициализации с некорректным значением"""
        # Значение меньше 0
        counter = SubtractorCounter(-5)
        self.assertEqual(counter.get_current_value_decimal(), COUNTER_MAX_VALUE)

        # Значение больше максимума
        counter = SubtractorCounter(100)
        self.assertEqual(counter.get_current_value_decimal(), COUNTER_MAX_VALUE)

    def test_countdown_sequence(self):
        """Тест последовательности вычитания"""
        counter = SubtractorCounter(7)
        expected_sequence = [7, 6, 5, 4, 3, 2, 1, 0, 7, 6, 5, 4, 3, 2, 1, 0]

        for expected in expected_sequence:
            self.assertEqual(counter.get_current_value_decimal(), expected)
            counter.tick()

    def test_binary_representation(self):
        """Тест двоичного представления"""
        counter = SubtractorCounter(7)
        expected_binary = ["111", "110", "101", "100", "011", "010", "001", "000"]

        for expected in expected_binary:
            self.assertEqual(counter.get_current_value_binary(), expected)
            counter.tick()

    def test_wrap_around(self):
        """Тест переполнения (возврат к 7 после 0)"""
        counter = SubtractorCounter(0)
        self.assertEqual(counter.get_current_value_decimal(), 0)

        counter.tick()
        self.assertEqual(counter.get_current_value_decimal(), COUNTER_MAX_VALUE)

        # Несколько переполнений подряд
        for _ in range(3):
            counter.tick()
        self.assertEqual(counter.get_current_value_decimal(), COUNTER_MAX_VALUE - 3)

    def test_full_cycle(self):
        """Тест полного цикла 0->7->6->...->0"""
        counter = SubtractorCounter(0)
        full_cycle = [0, 7, 6, 5, 4, 3, 2, 1, 0]

        for expected in full_cycle:
            self.assertEqual(counter.get_current_value_decimal(), expected)
            counter.tick()

    def test_multiple_cycles(self):
        """Тест нескольких полных циклов"""
        counter = SubtractorCounter(0)

        for cycle in range(5):
            for expected in [0, 7, 6, 5, 4, 3, 2, 1]:
                self.assertEqual(counter.get_current_value_decimal(), expected)
                counter.tick()

    def test_to_binary_3bit(self):
        """Тест статического метода преобразования в 3-битный двоичный код"""
        test_cases = [
            (0, "000"),
            (1, "001"),
            (2, "010"),
            (3, "011"),
            (4, "100"),
            (5, "101"),
            (6, "110"),
            (7, "111"),
        ]

        for value, expected in test_cases:
            with self.subTest(value=value):
                self.assertEqual(SubtractorCounter._to_binary_3bit(value), expected)


if __name__ == "__main__":
    unittest.main()
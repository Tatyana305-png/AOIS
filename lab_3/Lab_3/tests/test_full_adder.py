import unittest
from full_adder import FullAdder


class TestFullAdder(unittest.TestCase):
    """Тесты для одноразрядного полного сумматора (ОДС-3)"""

    def setUp(self):
        self.adder = FullAdder()

    def test_all_combinations(self):
        """Тест всех 8 комбинаций входов (3 бита)"""
        test_cases = [
            # (A, B, Cin) -> (Sum, Cout)
            (0, 0, 0, 0, 0),
            (0, 0, 1, 1, 0),
            (0, 1, 0, 1, 0),
            (0, 1, 1, 0, 1),
            (1, 0, 0, 1, 0),
            (1, 0, 1, 0, 1),
            (1, 1, 0, 0, 1),
            (1, 1, 1, 1, 1),
        ]

        for a, b, cin, expected_sum, expected_cout in test_cases:
            with self.subTest(a=a, b=b, cin=cin):
                self.adder.calculate(bool(a), bool(b), bool(cin))
                self.assertEqual(self.adder.get_sum(), bool(expected_sum))
                self.assertEqual(self.adder.get_carry_out(), bool(expected_cout))

    def test_sum_formula(self):
        """Проверка формулы Sum = A ⊕ B ⊕ Cin"""
        for a in [0, 1]:
            for b in [0, 1]:
                for cin in [0, 1]:
                    with self.subTest(a=a, b=b, cin=cin):
                        self.adder.calculate(bool(a), bool(b), bool(cin))
                        expected_sum = (a ^ b) ^ cin
                        self.assertEqual(self.adder.get_sum(), bool(expected_sum))

    def test_carry_formula(self):
        """Проверка формулы Cout = (A & B) | (Cin & (A ⊕ B))"""
        for a in [0, 1]:
            for b in [0, 1]:
                for cin in [0, 1]:
                    with self.subTest(a=a, b=b, cin=cin):
                        self.adder.calculate(bool(a), bool(b), bool(cin))
                        expected_cout = (a and b) or (cin and (a ^ b))
                        self.assertEqual(self.adder.get_carry_out(), bool(expected_cout))

    def test_multiple_calculations(self):
        """Проверка последовательных вычислений"""
        self.adder.calculate(True, True, False)
        self.assertEqual(self.adder.get_sum(), False)
        self.assertEqual(self.adder.get_carry_out(), True)

        self.adder.calculate(False, False, True)
        self.assertEqual(self.adder.get_sum(), True)
        self.assertEqual(self.adder.get_carry_out(), False)


if __name__ == "__main__":
    unittest.main()
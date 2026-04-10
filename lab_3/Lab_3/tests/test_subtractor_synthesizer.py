import unittest
from subtractor_synthesizer import SubtractorSynthesizer, LogicInBasisNAND_NOR
from constants import BITS_IN_3BIT_COUNTER


class TestSubtractorSynthesizer(unittest.TestCase):
    """Тесты для ВЫЧИТАЮЩЕГО счетчика на T-триггерах"""

    def setUp(self):
        self.counter = SubtractorSynthesizer()

    def test_initial_state(self):
        """Тест начального состояния"""
        self.assertEqual(self.counter.get_current_value(), 0)
        self.assertEqual(self.counter.get_binary(), "000")

    def test_t0_function(self):
        """Тест функции T0 (всегда True)"""
        for q2 in [False, True]:
            for q1 in [False, True]:
                for q0 in [False, True]:
                    with self.subTest(q2=q2, q1=q1, q0=q0):
                        self.assertTrue(self.counter._t0_function(q2, q1, q0))

    def test_t1_function(self):
        """Тест функции T1 = NOT Q0 (для вычитания)"""
        test_cases = [
            (False, False, False, True),  # not 0 = 1
            (False, False, True, False),  # not 1 = 0
            (False, True, False, True),
            (False, True, True, False),
            (True, False, False, True),
            (True, False, True, False),
            (True, True, False, True),
            (True, True, True, False),
        ]

        for q2, q1, q0, expected in test_cases:
            with self.subTest(q2=q2, q1=q1, q0=q0):
                self.assertEqual(self.counter._t1_function(q2, q1, q0), expected)

    def test_t2_function(self):
        """Тест функции T2 = (NOT Q0) AND (NOT Q1) (для вычитания)"""
        test_cases = [
            (False, False, False, True),  # not0 & not0 = 1 & 1 = 1
            (False, False, True, False),  # not1 & not0 = 0 & 1 = 0
            (False, True, False, False),  # not0 & not1 = 1 & 0 = 0
            (False, True, True, False),  # not1 & not1 = 0 & 0 = 0
            (True, False, False, True),
            (True, False, True, False),
            (True, True, False, False),
            (True, True, True, False),
        ]

        for q2, q1, q0, expected in test_cases:
            with self.subTest(q2=q2, q1=q1, q0=q0):
                self.assertEqual(self.counter._t2_function(q2, q1, q0), expected)

    def test_get_next_state(self):
        """Тест вычисления следующего состояния (ВЫЧИТАНИЕ)"""
        test_cases = [
            # (Q2, Q1, Q0) -> (Q2', Q1', Q0')
            (False, False, False, True, True, True),  # 0 -> 7
            (False, False, True, False, False, False),  # 1 -> 0
            (False, True, False, False, False, True),  # 2 -> 1
            (False, True, True, False, True, False),  # 3 -> 2
            (True, False, False, False, True, True),  # 4 -> 3
            (True, False, True, True, False, False),  # 5 -> 4
            (True, True, False, True, False, True),  # 6 -> 5
            (True, True, True, True, True, False),  # 7 -> 6
        ]

        for q2, q1, q0, next_q2, next_q1, next_q0 in test_cases:
            with self.subTest(current=(q2, q1, q0)):
                result = self.counter.get_next_state(q2, q1, q0)
                self.assertEqual(result, (next_q2, next_q1, next_q0))

    def test_tick_sequence(self):
        """Тест последовательности работы ВЫЧИТАЮЩЕГО счетчика"""
        # Вычитающий счетчик: 0->7->6->5->4->3->2->1->0...
        expected_sequence = [7, 6, 5, 4, 3, 2, 1, 0, 7, 6, 5, 4, 3, 2, 1, 0]

        for expected in expected_sequence:
            self.counter.tick()
            self.assertEqual(self.counter.get_current_value(), expected)

    def test_set_value(self):
        """Тест установки произвольного значения"""
        for value in range(8):
            with self.subTest(value=value):
                self.counter.set_value(value)
                self.assertEqual(self.counter.get_current_value(), value)
                self.assertEqual(
                    self.counter.get_binary(),
                    format(value, f"0{BITS_IN_3BIT_COUNTER}b")
                )

    def test_full_cycle(self):
        """Тест полного цикла вычитания"""
        self.counter.set_value(0)

        # После 0 должно стать 7 (вычитание с переполнением)
        self.counter.tick()
        self.assertEqual(self.counter.get_current_value(), 7)

        # Полный цикл от 7 до 0
        for expected in [6, 5, 4, 3, 2, 1, 0]:
            self.counter.tick()
            self.assertEqual(self.counter.get_current_value(), expected)

    def test_multiple_cycles(self):
        """Тест нескольких циклов подряд"""
        self.counter.set_value(0)

        for cycle in range(3):
            # После 0 должно стать 7
            self.counter.tick()
            self.assertEqual(self.counter.get_current_value(), 7)

            # Затем 6,5,4,3,2,1,0
            for expected in [6, 5, 4, 3, 2, 1, 0]:
                self.counter.tick()
                self.assertEqual(self.counter.get_current_value(), expected)

    def test_get_states(self):
        """Тест получения состояний триггеров"""
        self.counter.set_value(0)
        self.assertEqual(self.counter.get_states(), (False, False, False))

        self.counter.tick()  # 0 -> 7
        self.assertEqual(self.counter.get_states(), (True, True, True))

        self.counter.tick()  # 7 -> 6
        self.assertEqual(self.counter.get_states(), (True, True, False))

        self.counter.set_value(3)  # 011
        self.assertEqual(self.counter.get_states(), (False, True, True))

    def test_consistency_with_programmatic_counter(self):
        """Тест согласованности с программным вычитающим счетчиком"""
        from subtractor_counter import SubtractorCounter

        synthesized = SubtractorSynthesizer()
        programmatic = SubtractorCounter(0)

        # Оба счетчика должны показывать одинаковые значения
        # Вычитающая последовательность: 0,7,6,5,4,3,2,1,0,7,6,...
        for _ in range(16):
            self.assertEqual(
                synthesized.get_current_value(),
                programmatic.get_current_value_decimal()
            )
            synthesized.tick()
            programmatic.tick()


class TestLogicInBasisNAND_NOR(unittest.TestCase):
    """Тесты для демонстрации базиса НЕ-И-ИЛИ"""

    def test_nand(self):
        """Тест NAND (НЕ-И)"""
        self.assertTrue(LogicInBasisNAND_NOR.nand(False, False))
        self.assertTrue(LogicInBasisNAND_NOR.nand(True, False))
        self.assertTrue(LogicInBasisNAND_NOR.nand(False, True))
        self.assertFalse(LogicInBasisNAND_NOR.nand(True, True))

    def test_nor(self):
        """Тест NOR (НЕ-ИЛИ)"""
        self.assertTrue(LogicInBasisNAND_NOR.nor(False, False))
        self.assertFalse(LogicInBasisNAND_NOR.nor(True, False))
        self.assertFalse(LogicInBasisNAND_NOR.nor(False, True))
        self.assertFalse(LogicInBasisNAND_NOR.nor(True, True))

    def test_not_gate_nand(self):
        """Тест НЕ через NAND"""
        self.assertTrue(LogicInBasisNAND_NOR.not_gate_nand(False))
        self.assertFalse(LogicInBasisNAND_NOR.not_gate_nand(True))

    def test_not_gate_nor(self):
        """Тест НЕ через NOR"""
        self.assertTrue(LogicInBasisNAND_NOR.not_gate_nor(False))
        self.assertFalse(LogicInBasisNAND_NOR.not_gate_nor(True))

    def test_and_gate_nand(self):
        """Тест И через NAND"""
        self.assertFalse(LogicInBasisNAND_NOR.and_gate_nand(False, False))
        self.assertFalse(LogicInBasisNAND_NOR.and_gate_nand(True, False))
        self.assertFalse(LogicInBasisNAND_NOR.and_gate_nand(False, True))
        self.assertTrue(LogicInBasisNAND_NOR.and_gate_nand(True, True))

    def test_or_gate_nand(self):
        """Тест ИЛИ через NAND"""
        self.assertFalse(LogicInBasisNAND_NOR.or_gate_nand(False, False))
        self.assertTrue(LogicInBasisNAND_NOR.or_gate_nand(True, False))
        self.assertTrue(LogicInBasisNAND_NOR.or_gate_nand(False, True))
        self.assertTrue(LogicInBasisNAND_NOR.or_gate_nand(True, True))

    def test_xor_gate_nand(self):
        """Тест XOR через NAND"""
        self.assertFalse(LogicInBasisNAND_NOR.xor_gate_nand(False, False))
        self.assertTrue(LogicInBasisNAND_NOR.xor_gate_nand(True, False))
        self.assertTrue(LogicInBasisNAND_NOR.xor_gate_nand(False, True))
        self.assertFalse(LogicInBasisNAND_NOR.xor_gate_nand(True, True))

    def test_truth_table_equivalence(self):
        """Тест эквивалентности реализаций стандартным операторам"""
        for a in [False, True]:
            for b in [False, True]:
                with self.subTest(a=a, b=b):
                    self.assertEqual(
                        LogicInBasisNAND_NOR.and_gate_nand(a, b),
                        a and b
                    )
                    self.assertEqual(
                        LogicInBasisNAND_NOR.or_gate_nand(a, b),
                        a or b
                    )
                    self.assertEqual(
                        LogicInBasisNAND_NOR.xor_gate_nand(a, b),
                        a ^ b
                    )


if __name__ == "__main__":
    unittest.main()
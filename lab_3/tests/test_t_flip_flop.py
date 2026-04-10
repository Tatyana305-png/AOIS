import unittest
from t_flip_flop import TFlipFlop, TFlipFlopWithLogic


class TestTFlipFlop(unittest.TestCase):
    """Тесты для T-триггера"""

    def setUp(self):
        self.ff = TFlipFlop(False)

    def test_initial_state(self):
        """Тест начального состояния"""
        ff_false = TFlipFlop(False)
        ff_true = TFlipFlop(True)

        self.assertFalse(ff_false.get_state())
        self.assertTrue(ff_true.get_state())

    def test_characteristic_equation(self):
        """Тест характеристического уравнения Q_next = T ⊕ Q"""
        # T=0, Q=0 -> Q_next=0
        self.assertFalse(TFlipFlopWithLogic.characteristic_equation(False, False))
        # T=0, Q=1 -> Q_next=1
        self.assertTrue(TFlipFlopWithLogic.characteristic_equation(False, True))
        # T=1, Q=0 -> Q_next=1
        self.assertTrue(TFlipFlopWithLogic.characteristic_equation(True, False))
        # T=1, Q=1 -> Q_next=0
        self.assertFalse(TFlipFlopWithLogic.characteristic_equation(True, True))

    def test_tick_behavior(self):
        """Тест поведения при тактовых импульсах"""
        self.ff.set_state(False)

        # T=0, состояние не меняется
        self.ff.tick(False)
        self.assertFalse(self.ff.get_state())

        # T=1, состояние инвертируется
        self.ff.tick(True)
        self.assertTrue(self.ff.get_state())

        # T=1, снова инвертируется
        self.ff.tick(True)
        self.assertFalse(self.ff.get_state())

        # T=0, не меняется
        self.ff.tick(False)
        self.assertFalse(self.ff.get_state())

    def test_all_combinations(self):
        """Тест всех комбинаций T и начального состояния"""
        for initial in [False, True]:
            for t in [False, True, False, True]:
                with self.subTest(initial=initial, t=t):
                    ff = TFlipFlop(initial)
                    expected = t ^ initial
                    ff.tick(t)
                    self.assertEqual(ff.get_state(), expected)

    def test_reset(self):
        """Тест сброса триггера"""
        self.ff.set_state(True)
        self.assertTrue(self.ff.get_state())

        self.ff.reset()
        self.assertFalse(self.ff.get_state())

        self.ff.set_state(True)
        self.ff.tick(True)
        self.assertFalse(self.ff.get_state())
        self.ff.reset()
        self.assertFalse(self.ff.get_state())

    def test_get_state_int(self):
        """Тест получения состояния как int"""
        self.ff.set_state(False)
        self.assertEqual(self.ff.get_state_int(), 0)

        self.ff.set_state(True)
        self.assertEqual(self.ff.get_state_int(), 1)

    def test_compute_next_state(self):
        """Тест вычисления следующего состояния без обновления"""
        ff_logic = TFlipFlopWithLogic()
        ff_logic.current_state = False

        self.assertTrue(ff_logic.compute_next_state(True))
        self.assertFalse(ff_logic.compute_next_state(False))

        ff_logic.current_state = True
        self.assertFalse(ff_logic.compute_next_state(True))
        self.assertTrue(ff_logic.compute_next_state(False))

    def test_update(self):
        """Тест обновления состояния"""
        ff_logic = TFlipFlopWithLogic()
        ff_logic.current_state = False

        ff_logic.update(True)
        self.assertTrue(ff_logic.current_state)
        self.assertTrue(ff_logic.get_t_input())

        ff_logic.update(False)
        self.assertTrue(ff_logic.current_state)

    def test_repr(self):
        """Тест строкового представления"""
        ff_logic = TFlipFlopWithLogic("test", False)
        self.assertEqual(repr(ff_logic), "TFlipFlop(test: Q=0)")

        ff_logic.update(True)
        self.assertEqual(repr(ff_logic), "TFlipFlop(test: Q=1)")


if __name__ == "__main__":
    unittest.main()
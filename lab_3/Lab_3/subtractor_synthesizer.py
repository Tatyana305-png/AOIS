"""
Синтез ВЫЧИТАЮЩЕГО счетчика на 8 состояний (3 бита)
в базисе НЕ-И-ИЛИ на T-триггерах.
"""

from t_flip_flop import TFlipFlop
from constants import BITS_IN_3BIT_COUNTER


class SubtractorSynthesizer:
    """
    ВЫЧИТАЮЩИЙ счетчик на T-триггерах.
    Переходы: 7→6→5→4→3→2→1→0→7
    """

    def __init__(self) -> None:
        self.t_flip_flops = [TFlipFlop(False) for _ in range(BITS_IN_3BIT_COUNTER)]
        self.current_value = 0

    # ============= ЛОГИКА В БАЗИСЕ НЕ-И-ИЛИ =============

    @staticmethod
    def _not_gate(a: bool) -> bool:
        return not a

    @staticmethod
    def _and_gate(a: bool, b: bool) -> bool:
        return a and b

    @staticmethod
    def _or_gate(a: bool, b: bool) -> bool:
        return a or b

    # ============= ФУНКЦИИ ВОЗБУЖДЕНИЯ ДЛЯ ВЫЧИТАЮЩЕГО СЧЕТЧИКА =============

    def _t0_function(self, q2: bool, q1: bool, q0: bool) -> bool:
        """
        T0 = 1 (всегда переключается)
        """
        return True

    def _t1_function(self, q2: bool, q1: bool, q0: bool) -> bool:
        """
        T1 = NOT Q0 (для вычитания)
        """
        return not q0

    def _t2_function(self, q2: bool, q1: bool, q0: bool) -> bool:
        """
        T2 = (NOT Q0) AND (NOT Q1) (для вычитания)
        """
        return (not q0) and (not q1)

    # Альтернативная реализация через NAND
    def _t2_function_nand(self, q2: bool, q1: bool, q0: bool) -> bool:
        """
        T2 через NAND: T2 = NOT (Q0 OR Q1)
        """
        def nand(a: bool, b: bool) -> bool:
            return not (a and b)

        def nor(a: bool, b: bool) -> bool:
            return not (a or b)

        # Q0 NOR Q1 = NOT (Q0 OR Q1)
        return nor(q0, q1)

    # ============= ВЫЧИСЛЕНИЕ СЛЕДУЮЩЕГО СОСТОЯНИЯ =============

    def get_next_state(self, q2: bool, q1: bool, q0: bool) -> tuple[bool, bool, bool]:
        """Вычислить следующее состояние по текущему"""
        t0 = self._t0_function(q2, q1, q0)
        t1 = self._t1_function(q2, q1, q0)
        t2 = self._t2_function(q2, q1, q0)

        next_q0 = t0 ^ q0
        next_q1 = t1 ^ q1
        next_q2 = t2 ^ q2

        return next_q2, next_q1, next_q0

    def tick(self) -> None:
        """Один такт работы счетчика (вычитание)"""
        q2 = self.t_flip_flops[2].get_state()
        q1 = self.t_flip_flops[1].get_state()
        q0 = self.t_flip_flops[0].get_state()

        t0 = self._t0_function(q2, q1, q0)
        t1 = self._t1_function(q2, q1, q0)
        t2 = self._t2_function(q2, q1, q0)

        self.t_flip_flops[0].tick(t0)
        self.t_flip_flops[1].tick(t1)
        self.t_flip_flops[2].tick(t2)

        self._update_current_value()

    def _update_current_value(self) -> None:
        """Обновить десятичное значение"""
        value = 0
        for i, ff in enumerate(self.t_flip_flops):
            if ff.get_state():
                value |= (1 << i)
        self.current_value = value

    def set_value(self, value: int) -> None:
        """Принудительно установить значение счетчика (0-7)"""
        if 0 <= value <= 7:
            for i in range(BITS_IN_3BIT_COUNTER):
                bit_value = bool((value >> i) & 1)
                self.t_flip_flops[i].set_state(bit_value)
            self.current_value = value

    def get_current_value(self) -> int:
        return self.current_value

    def get_binary(self) -> str:
        """Получить двоичное представление (Q2 Q1 Q0)"""
        bits = [str(ff.get_state_int()) for ff in reversed(self.t_flip_flops)]
        return "".join(bits)

    def get_states(self) -> tuple[bool, bool, bool]:
        return (
            self.t_flip_flops[2].get_state(),
            self.t_flip_flops[1].get_state(),
            self.t_flip_flops[0].get_state(),
        )

    def print_transition_table(self) -> None:
        """Вывести таблицу переходов"""
        print("\n" + "=" * 60)
        print("Таблица переходов ВЫЧИТАЮЩЕГО счетчика (T-триггеры)")
        print("=" * 60)
        print(" Q2 Q1 Q0 | T2 T1 T0 | Q2' Q1' Q0' | Decimal")
        print("-" * 60)

        for dec in range(8):
            q2 = bool((dec >> 2) & 1)
            q1 = bool((dec >> 1) & 1)
            q0 = bool(dec & 1)

            t2 = self._t2_function(q2, q1, q0)
            t1 = self._t1_function(q2, q1, q0)
            t0 = self._t0_function(q2, q1, q0)

            next_q2, next_q1, next_q0 = self.get_next_state(q2, q1, q0)
            next_dec = (next_q2 << 2) | (next_q1 << 1) | next_q0

            print(
                f" {int(q2)}  {int(q1)}  {int(q0)}  |  {int(t2)}  {int(t1)}  {int(t0)}  |  "
                f" {int(next_q2)}   {int(next_q1)}   {int(next_q0)}  |    {dec} -> {next_dec}"
            )

        print("=" * 60)


class LogicInBasisNAND_NOR:
    """Демонстрация реализации логических функций в базисе НЕ-И-ИЛИ"""

    @staticmethod
    def nand(a: bool, b: bool) -> bool:
        return not (a and b)

    @staticmethod
    def nor(a: bool, b: bool) -> bool:
        return not (a or b)

    @staticmethod
    def not_gate_nand(x: bool) -> bool:
        return not (x and x)

    @staticmethod
    def not_gate_nor(x: bool) -> bool:
        return not (x or x)

    @staticmethod
    def and_gate_nand(a: bool, b: bool) -> bool:
        return not (not (a and b))

    @staticmethod
    def or_gate_nand(a: bool, b: bool) -> bool:
        not_a = not (a and a)
        not_b = not (b and b)
        return not (not_a and not_b)

    @staticmethod
    def xor_gate_nand(a: bool, b: bool) -> bool:
        nand_ab = not (a and b)
        nand_a_nand = not (a and nand_ab)
        nand_b_nand = not (b and nand_ab)
        return not (nand_a_nand and nand_b_nand)

    @staticmethod
    def demonstrate() -> None:
        print("\n" + "=" * 60)
        print("Демонстрация базиса НЕ-И-ИЛИ")
        print("=" * 60)
        a, b = True, False
        print(f"a={a}, b={b}")
        print(f"  NAND(a,b) = {LogicInBasisNAND_NOR.nand(a, b)}")
        print(f"  NOR(a,b)  = {LogicInBasisNAND_NOR.nor(a, b)}")
        print(f"  NOT a (через NAND) = {LogicInBasisNAND_NOR.not_gate_nand(a)}")
        print(f"  a AND b (через NAND) = {LogicInBasisNAND_NOR.and_gate_nand(a, b)}")
        print(f"  a OR b (через NAND) = {LogicInBasisNAND_NOR.or_gate_nand(a, b)}")
        print(f"  a XOR b (через NAND) = {LogicInBasisNAND_NOR.xor_gate_nand(a, b)}")
        print("=" * 60)
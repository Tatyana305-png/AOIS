from constants import BITS_IN_TETRAD
from full_adder import FullAdder


class ParallelAdder:
    def __init__(self) -> None:
        self.adders = [FullAdder() for _ in range(BITS_IN_TETRAD)]
        self.result_bits = [False] * BITS_IN_TETRAD
        self.final_carry = False

    @staticmethod
    def _char_to_bool(bit: str) -> bool:
        return bit == "1"

    @staticmethod
    def _validate_binary(binary_value: str) -> None:
        if len(binary_value) != BITS_IN_TETRAD:
            raise ValueError(f"Binary value must contain {BITS_IN_TETRAD} bits")
        if any(bit not in {"0", "1"} for bit in binary_value):
            raise ValueError("Binary value must contain only 0 and 1")

    def process_addition(
        self,
        binary_a: str,
        binary_b: str,
        initial_carry: bool,
    ) -> None:
        self._validate_binary(binary_a)
        self._validate_binary(binary_b)

        current_carry = initial_carry
        for index in range(BITS_IN_TETRAD - 1, -1, -1):
            self.adders[index].calculate(
                self._char_to_bool(binary_a[index]),
                self._char_to_bool(binary_b[index]),
                current_carry,
            )
            self.result_bits[index] = self.adders[index].get_sum()
            current_carry = self.adders[index].get_carry_out()

        self.final_carry = current_carry

    def get_result_string(self) -> str:
        return "".join("1" if bit else "0" for bit in self.result_bits)

    def get_final_carry(self) -> bool:
        return self.final_carry

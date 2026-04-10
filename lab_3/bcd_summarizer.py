from constants import BCD_OFFSET, BITS_IN_TETRAD


class BCDSummarizer:
    def __init__(self) -> None:
        self.tens_digit = "0000"
        self.units_digit = "0000"

    @staticmethod
    def _validate_binary(binary_value: str) -> None:
        if len(binary_value) != BITS_IN_TETRAD:
            raise ValueError(f"BCD digit must contain {BITS_IN_TETRAD} bits")
        if any(bit not in {"0", "1"} for bit in binary_value):
            raise ValueError("BCD digit must contain only 0 and 1")

    @staticmethod
    def _string_to_int(binary_value: str) -> int:
        return int(binary_value, 2)

    @staticmethod
    def _int_to_binary_4bit(value: int) -> str:
        return format(value, "04b")

    def execute(self, bcd_a: str, bcd_b: str) -> None:
        self._validate_binary(bcd_a)
        self._validate_binary(bcd_b)

        value_a = self._string_to_int(bcd_a)
        value_b = self._string_to_int(bcd_b)
        raw_sum = value_a + value_b + BCD_OFFSET

        units = raw_sum % 10
        tens = raw_sum // 10

        self.units_digit = self._int_to_binary_4bit(units)
        self.tens_digit = self._int_to_binary_4bit(tens)

    def get_full_result(self) -> str:
        return f"{self.tens_digit} {self.units_digit}"

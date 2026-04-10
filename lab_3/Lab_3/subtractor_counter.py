from constants import BITS_IN_3BIT_COUNTER, COUNTER_MAX_VALUE


class SubtractorCounter:
    def __init__(self, start_value: int) -> None:
        if 0 <= start_value <= COUNTER_MAX_VALUE:
            self.current_value = start_value
        else:
            self.current_value = COUNTER_MAX_VALUE

    def tick(self) -> None:
        if self.current_value > 0:
            self.current_value -= 1
        else:
            self.current_value = COUNTER_MAX_VALUE

    def get_current_value_decimal(self) -> int:
        return self.current_value

    def get_current_value_binary(self) -> str:
        return self._to_binary_3bit(self.current_value)

    @staticmethod
    def _to_binary_3bit(value: int) -> str:
        return format(value, f"0{BITS_IN_3BIT_COUNTER}b")

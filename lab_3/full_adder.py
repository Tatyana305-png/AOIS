class FullAdder:
    def __init__(self) -> None:
        self.sum = False
        self.carry_out = False

    def calculate(self, bit_a: bool, bit_b: bool, carry_in: bool) -> None:
        self.sum = (bit_a ^ bit_b) ^ carry_in
        self.carry_out = (bit_a and bit_b) or (carry_in and (bit_a ^ bit_b))

    def get_sum(self) -> bool:
        return self.sum

    def get_carry_out(self) -> bool:
        return self.carry_out

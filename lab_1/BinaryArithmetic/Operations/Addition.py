from Codes.AdditionalCode import AdditionalCode


class Addition:
    """Операция сложения в дополнительном коде"""

    def __init__(self, bits=32):
        self.bits = bits
        self.additional_code = AdditionalCode(bits)

    def execute(self, num1, num2):
        """Выполнение сложения"""
        add1 = self.additional_code.to_binary(num1)
        add2 = self.additional_code.to_binary(num2)

        result = [0] * self.bits
        carry = 0

        for i in range(self.bits - 1, -1, -1):
            total = add1[i] + add2[i] + carry
            result[i] = total % 2
            carry = total // 2

        # Преобразование результата обратно в десятичное число
        dec_result = self.additional_code.from_binary(result)

        return result, dec_result
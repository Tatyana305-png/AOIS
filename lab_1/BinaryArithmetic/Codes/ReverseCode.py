from .DirectCode import DirectCode


class ReverseCode(DirectCode):
    """Обратный код числа"""

    def to_binary(self, number):
        """Преобразование в обратный код"""
        if number >= 0:
            return super().to_binary(number)
        else:
            direct = super().to_binary(number)
            # Инвертируем все биты кроме знакового
            reverse = direct.copy()
            for i in range(1, self.bits):
                reverse[i] = 1 - reverse[i]
            return reverse

    def from_binary(self, bits_array):
        """Преобразование из обратного кода"""
        if bits_array[0] == 0:
            return super().from_binary(bits_array)
        else:
            # Инвертируем обратно
            direct = bits_array.copy()
            for i in range(1, self.bits):
                direct[i] = 1 - direct[i]
            return super().from_binary(direct)
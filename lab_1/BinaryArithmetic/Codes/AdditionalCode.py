from .ReverseCode import ReverseCode


class AdditionalCode(ReverseCode):
    """Дополнительный код числа"""

    def to_binary(self, number):
        """Преобразование в дополнительный код"""
        if number >= 0:
            return super().to_binary(number)
        else:
            unsigned = (1 << self.bits) + number
            return self._to_unsigned_binary(unsigned)

    def from_binary(self, bits_array):
        """Преобразование из дополнительного кода"""
        unsigned = self._from_unsigned_binary(bits_array)

        # Если число в диапазоне отрицательных (старший бит = 1)
        if bits_array[0] == 1:
            # Преобразуем обратно в отрицательное
            return unsigned - (1 << self.bits)
        else:
            return unsigned
from Converters.BinaryConverter import BinaryConverter


class DirectCode(BinaryConverter):
    """Прямой код числа"""

    def to_binary(self, number):
        """Преобразование в прямой код"""
        if number >= 0:
            return self._to_unsigned_binary(number)
        else:
            bits_array = self._to_unsigned_binary(abs(number))
            bits_array[0] = 1
            return bits_array

    def from_binary(self, bits_array):
        """Преобразование из прямого кода"""
        sign = bits_array[0]
        magnitude = bits_array.copy()
        magnitude[0] = 0
        result = self._from_unsigned_binary(magnitude)
        return -result if sign else result
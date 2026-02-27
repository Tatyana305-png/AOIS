from .BinaryConverter import BinaryConverter


class FloatConverter(BinaryConverter):
    """Конвертер для чисел с плавающей точкой по стандарту IEEE-754"""

    def __init__(self):
        super().__init__(32)
        self.exponent_bits = 8
        self.mantissa_bits = 23
        self.bias = 127

    def to_binary(self, number):
        """Преобразование числа в формат IEEE-754"""
        if number == 0:
            return [0] * self.bits

        # Определяем знак
        sign = 0 if number >= 0 else 1
        number = abs(number)

        # Нормализация
        exponent = 0
        if number >= 2.0:
            while number >= 2.0:
                number /= 2
                exponent += 1
        elif number < 1.0:
            while number < 1.0:
                number *= 2
                exponent -= 1

        # Смещение экспоненты
        exponent += self.bias

        # Получаем мантиссу
        mantissa = number - 1.0
        mantissa_bits = []
        for _ in range(self.mantissa_bits):
            mantissa *= 2
            if mantissa >= 1.0:
                mantissa_bits.append(1)
                mantissa -= 1.0
            else:
                mantissa_bits.append(0)

        # Формируем результат
        result = [sign]
        exp_bits = self._to_unsigned_binary(exponent)[self.bits - self.exponent_bits:]
        result.extend(exp_bits)
        result.extend(mantissa_bits)

        return result

    def from_binary(self, bits_array):
        """Преобразование из формата IEEE-754 в десятичное число"""
        sign = bits_array[0]

        # Извлекаем экспоненту
        exponent = 0
        for i in range(1, self.exponent_bits + 1):
            exponent = (exponent << 1) | bits_array[i]
        exponent -= self.bias

        # Извлекаем мантиссу
        mantissa = 1.0
        for i in range(self.exponent_bits + 1, self.bits):
            mantissa += bits_array[i] * (2 ** (self.exponent_bits - i))

        result = mantissa * (2 ** exponent)
        return -result if sign else result
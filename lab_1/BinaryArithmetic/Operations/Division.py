from Codes.DirectCode import DirectCode
from Converters.FloatConverter import FloatConverter


class Division:
    """Операция деления в прямом коде"""

    def __init__(self, bits=32, precision=5):
        self.bits = bits
        self.precision = precision
        self.direct_code = DirectCode(bits)
        self.float_converter = FloatConverter()

    def execute(self, num1, num2):
        """Выполнение деления"""
        if num2 == 0:
            raise ValueError("Деление на ноль!")

        direct1 = self.direct_code.to_binary(num1)
        direct2 = self.direct_code.to_binary(num2)

        # Определяем знак результата
        sign = direct1[0] ^ direct2[0]

        # Берем модули чисел
        dividend = abs(num1)
        divisor = abs(num2)

        # Целая часть
        quotient_int = dividend // divisor
        remainder = dividend % divisor

        # Дробная часть с заданной точностью
        fraction = []
        for _ in range(self.precision):
            remainder *= 10
            digit = remainder // divisor
            fraction.append(digit)
            remainder = remainder % divisor

        # Формируем результат
        result_dec = float(f"{quotient_int}.{''.join(map(str, fraction))}")
        if sign:
            result_dec = -result_dec

        # Представление в двоичном виде
        result_binary = self.float_converter.to_binary(result_dec)

        return result_binary, result_dec
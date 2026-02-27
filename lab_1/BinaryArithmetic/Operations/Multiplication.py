from Codes.DirectCode import DirectCode


class Multiplication:
    """Операция умножения в прямом коде"""

    def __init__(self, bits=32):
        self.bits = bits
        self.direct_code = DirectCode(bits)

    def execute(self, num1, num2):
        """Выполнение умножения"""
        # Определяем знак результата
        sign = -1 if (num1 < 0) ^ (num2 < 0) else 1

        # Берем модули чисел
        a = abs(num1)
        b = abs(num2)

        # Выполняем умножение обычным способом
        result_dec = a * b * sign

        # Получаем двоичное представление в прямом коде
        result_binary = self.direct_code.to_binary(result_dec)

        return result_binary, result_dec
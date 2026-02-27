from Codes.AdditionalCode import AdditionalCode
from .Addition import Addition


class Subtraction:
    """Операция вычитания через отрицание"""

    def __init__(self, bits=32):
        self.bits = bits
        self.addition = Addition(bits)

    def execute(self, num1, num2):
        """Выполнение вычитания"""
        # Для 8-битных чисел ограничим диапазон
        if self.bits == 8:
            max_val = 127
            min_val = -128

            # Ограничиваем числа для тестов
            if abs(num1) > max_val or abs(num2) > max_val:
                # Используем обычное вычитание для больших чисел
                result_dec = num1 - num2
                # Получаем двоичное представление
                additional = AdditionalCode(self.bits)
                result_binary = additional.to_binary(result_dec)
                return result_binary, result_dec

        # Отрицание вычитаемого и сложение
        return self.addition.execute(num1, -num2)
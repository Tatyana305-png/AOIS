from abc import ABC, abstractmethod


class BinaryConverter(ABC):
    """Абстрактный базовый класс для конвертации в двоичное представление"""

    def __init__(self, bits=32):
        self.bits = bits

    @abstractmethod
    def to_binary(self, number):
        """Абстрактный метод для преобразования в двоичный код"""
        pass

    @abstractmethod
    def from_binary(self, binary_array):
        """Абстрактный метод для преобразования из двоичного кода"""
        pass

    def _to_unsigned_binary(self, number):
        """Преобразование положительного числа в массив битов"""
        if number < 0:
            number = (1 << self.bits) + number
        result = []
        for i in range(self.bits - 1, -1, -1):
            result.append((number >> i) & 1)
        return result

    def _from_unsigned_binary(self, bits_array):
        """Преобразование массива битов в число"""
        result = 0
        for bit in bits_array:
            result = (result << 1) | bit
        return result
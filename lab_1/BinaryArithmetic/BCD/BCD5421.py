class BCD5421:
    """Класс для работы с 5421 BCD кодом"""

    def __init__(self):
        # Таблица кодирования 5421 (веса: 5-4-2-1)
        self.encode_table = {
            0: [0, 0, 0, 0],
            1: [0, 0, 0, 1],
            2: [0, 0, 1, 0],
            3: [0, 0, 1, 1],
            4: [0, 1, 0, 0],
            5: [1, 0, 0, 0],
            6: [1, 0, 0, 1],
            7: [1, 0, 1, 0],
            8: [1, 0, 1, 1],
            9: [1, 1, 0, 0],
        }

        self.decode_table = {tuple(v): k for k, v in self.encode_table.items()}

    def to_bcd(self, number):
        """Преобразование числа в 5421 BCD код"""
        if number < 0 or number > 9999:
            raise ValueError("Число должно быть от 0 до 9999")

        thousands = number // 1000
        hundreds = (number // 100) % 10
        tens = (number // 10) % 10
        units = number % 10

        result = []
        result.extend(self.encode_table[thousands])
        result.extend(self.encode_table[hundreds])
        result.extend(self.encode_table[tens])
        result.extend(self.encode_table[units])

        return result

    def from_bcd(self, bcd_array):
        """Преобразование из 5421 BCD в десятичное"""
        if len(bcd_array) != 16:
            raise ValueError("Должно быть 16 бит")

        thousands_code = tuple(bcd_array[0:4])
        hundreds_code = tuple(bcd_array[4:8])
        tens_code = tuple(bcd_array[8:12])
        units_code = tuple(bcd_array[12:16])

        thousands = self.decode_table.get(thousands_code, 0)
        hundreds = self.decode_table.get(hundreds_code, 0)
        tens = self.decode_table.get(tens_code, 0)
        units = self.decode_table.get(units_code, 0)

        return thousands * 1000 + hundreds * 100 + tens * 10 + units

    def add(self, num1, num2):
        """Сложение чисел в 5421 BCD коде"""
        if num1 + num2 > 9999:
            raise ValueError("Результат превышает 9999")

        result_dec = num1 + num2
        result_bcd = self.to_bcd(result_dec)

        return result_bcd, result_dec
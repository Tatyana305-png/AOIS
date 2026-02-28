from Converters.FloatConverter import FloatConverter
from Codes.DirectCode import DirectCode
from Codes.ReverseCode import ReverseCode
from Codes.AdditionalCode import AdditionalCode
from Operations.Addition import Addition
from Operations.Subtraction import Subtraction
from Operations.Multiplication import Multiplication
from Operations.Division import Division
from BCD.BCD5421 import BCD5421
from Utils.BinaryPrinter import BinaryPrinter


class BinaryArithmeticLab:
    """Главный класс лабораторной работы"""

    def __init__(self):
        self.bits = 32
        self.printer = BinaryPrinter()

        self.direct_code = DirectCode(self.bits)
        self.reverse_code = ReverseCode(self.bits)
        self.additional_code = AdditionalCode(self.bits)
        self.float_converter = FloatConverter()

        self.addition = Addition(self.bits)
        self.subtraction = Subtraction(self.bits)
        self.multiplication = Multiplication(self.bits)
        self.division = Division(self.bits, precision=5)

        self.bcd_5421 = BCD5421()

    def run_task1(self, numbers):
        """Задание 1: Перевод в разные коды"""
        self.printer.print_section("1. ПЕРЕВОД ЧИСЕЛ В РАЗНЫЕ КОДЫ")

        for num in numbers:
            direct = self.direct_code.to_binary(num)
            reverse = self.reverse_code.to_binary(num)
            additional = self.additional_code.to_binary(num)

            self.printer.print_number_conversion(num, direct, reverse, additional)

    def run_task2(self, num1, num2):
        """Задание 2: Сложение в дополнительном коде"""
        self.printer.print_section("2. СЛОЖЕНИЕ В ДОПОЛНИТЕЛЬНОМ КОДЕ")
        result_bin, result_dec = self.addition.execute(num1, num2)
        self.printer.print_operation(f"{num1} + {num2}", num1, num2, result_bin, result_dec)

    def run_task3(self, num1, num2):
        """Задание 3: Вычитание через отрицание"""
        self.printer.print_section("3. ВЫЧИТАНИЕ ЧЕРЕЗ ОТРИЦАНИЕ")
        result_bin, result_dec = self.subtraction.execute(num1, num2)
        self.printer.print_operation(f"{num1} - {num2}", num1, num2, result_bin, result_dec)

    def run_task4(self, num1, num2):
        """Задание 4: Умножение в прямом коде"""
        self.printer.print_section("4. УМНОЖЕНИЕ В ПРЯМОМ КОДЕ")
        result_bin, result_dec = self.multiplication.execute(num1, num2)
        self.printer.print_operation(f"{num1} * {num2}", num1, num2, result_bin, result_dec)

    def run_task5(self, num1, num2):
        """Задание 5: Деление в прямом коде"""
        self.printer.print_section("5. ДЕЛЕНИЕ В ПРЯМОМ КОДЕ")
        result_bin, result_dec = self.division.execute(num1, num2)
        self.printer.print_operation(f"{num1} / {num2}", num1, num2, result_bin, result_dec)

    def run_task6(self, num1, num2):
        """Задание 6: Операции с плавающей точкой"""
        self.printer.print_section("6. ОПЕРАЦИИ С ПЛАВАЮЩЕЙ ТОЧКОЙ IEEE-754")

        print(f"\nЧисло 1: {num1}")
        print(f"Число 2: {num2}")

        result_bin = self.float_converter.to_binary(num1 + num2)
        self.printer.print_float_operation(f"{num1} + {num2}", num1, num2, result_bin, num1 + num2)

        result_bin = self.float_converter.to_binary(num1 - num2)
        self.printer.print_float_operation(f"{num1} - {num2}", num1, num2, result_bin, num1 - num2)

        result_bin = self.float_converter.to_binary(num1 * num2)
        self.printer.print_float_operation(f"{num1} * {num2}", num1, num2, result_bin, num1 * num2)

        if num2 != 0:
            result_bin = self.float_converter.to_binary(num1 / num2)
            self.printer.print_float_operation(f"{num1} / {num2}", num1, num2, result_bin, num1 / num2)

    def run_task7(self, num1, num2):
        """Задание 7: 5421 BCD код"""
        self.printer.print_section("7. 5421 BCD КОД")

        print(f"\nЧисло 1: {num1}")
        print(f"Число 2: {num2}")

        bcd1 = self.bcd_5421.to_bcd(num1)
        bcd2 = self.bcd_5421.to_bcd(num2)

        self.printer.print_binary(bcd1, f"{num1} в 5421 BCD")
        self.printer.print_binary(bcd2, f"{num2} в 5421 BCD")

        # Сложение
        result_bin, result_dec = self.bcd_5421.add(num1, num2)
        self.printer.print_operation(f"{num1} + {num2}", num1, num2, result_bin, result_dec)

    def run_all(self):
        """Запуск всех заданий с тестовыми данными"""

        test_numbers = [45, -23, 127, -128]
        a, b = 45, -23
        c, d = 15, 3
        f1, f2 = 12.5, 3.75
        bcd1, bcd2 = 123, 456

        self.run_task1(test_numbers[:2])
        self.run_task2(a, b)
        self.run_task3(a, b)
        self.run_task4(c, d)
        self.run_task5(c, d)
        self.run_task6(f1, f2)
        self.run_task7(bcd1, bcd2)



if __name__ == "__main__":
    lab = BinaryArithmeticLab()

    lab.run_all()

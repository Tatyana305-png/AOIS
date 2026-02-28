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

    def get_integer_input(self, prompt):
        """Безопасный ввод целого числа"""
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Ошибка! Введите целое число.")

    def get_float_input(self, prompt):
        """Безопасный ввод числа с плавающей точкой"""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Ошибка! Введите число.")

    def get_bcd_input(self, prompt):
        """Безопасный ввод числа для BCD (0-9999)"""
        while True:
            try:
                num = int(input(prompt))
                if 0 <= num <= 9999:
                    return num
                else:
                    print("Ошибка! Число должно быть от 0 до 9999.")
            except ValueError:
                print("Ошибка! Введите целое число.")

    def run_task1_interactive(self):
        """Задание 1: Перевод в разные коды (интерактивно)"""
        self.printer.print_section("1. ПЕРЕВОД ЧИСЕЛ В РАЗНЫЕ КОДЫ")

        print("Введите числа для перевода (для выхода введите 'q'):")
        while True:
            try:
                user_input = input("\nВведите число (или 'q' для выхода): ")
                if user_input.lower() == 'q':
                    break

                num = int(user_input)
                direct = self.direct_code.to_binary(num)
                reverse = self.reverse_code.to_binary(num)
                additional = self.additional_code.to_binary(num)

                self.printer.print_number_conversion(num, direct, reverse, additional)

            except ValueError:
                print("Ошибка! Введите целое число.")
            except Exception as e:
                print(f"Ошибка: {e}")

    def run_task2_interactive(self):
        """Задание 2: Сложение в дополнительном коде (интерактивно)"""
        self.printer.print_section("2. СЛОЖЕНИЕ В ДОПОЛНИТЕЛЬНОМ КОДЕ")

        print("Введите два числа для сложения:")
        num1 = self.get_integer_input("Первое число: ")
        num2 = self.get_integer_input("Второе число: ")

        result_bin, result_dec = self.addition.execute(num1, num2)
        self.printer.print_operation(f"{num1} + {num2}", num1, num2, result_bin, result_dec)

    def run_task3_interactive(self):
        """Задание 3: Вычитание через отрицание (интерактивно)"""
        self.printer.print_section("3. ВЫЧИТАНИЕ ЧЕРЕЗ ОТРИЦАНИЕ")

        print("Введите два числа для вычитания (уменьшаемое - вычитаемое):")
        num1 = self.get_integer_input("Уменьшаемое: ")
        num2 = self.get_integer_input("Вычитаемое: ")

        result_bin, result_dec = self.subtraction.execute(num1, num2)
        self.printer.print_operation(f"{num1} - {num2}", num1, num2, result_bin, result_dec)

    def run_task4_interactive(self):
        """Задание 4: Умножение в прямом коде (интерактивно)"""
        self.printer.print_section("4. УМНОЖЕНИЕ В ПРЯМОМ КОДЕ")

        print("Введите два числа для умножения:")
        num1 = self.get_integer_input("Первое число: ")
        num2 = self.get_integer_input("Второе число: ")

        result_bin, result_dec = self.multiplication.execute(num1, num2)
        self.printer.print_operation(f"{num1} * {num2}", num1, num2, result_bin, result_dec)

    def run_task5_interactive(self):
        """Задание 5: Деление в прямом коде (интерактивно)"""
        self.printer.print_section("5. ДЕЛЕНИЕ В ПРЯМОМ КОДЕ")

        print("Введите два числа для деления (делимое / делитель):")
        num1 = self.get_integer_input("Делимое: ")

        while True:
            num2 = self.get_integer_input("Делитель: ")
            if num2 != 0:
                break
            print("Ошибка! Делитель не может быть равен 0.")

        try:
            result_bin, result_dec = self.division.execute(num1, num2)
            self.printer.print_operation(f"{num1} / {num2}", num1, num2, result_bin, result_dec)
        except Exception as e:
            print(f"Ошибка при делении: {e}")

    def run_task6_interactive(self):
        """Задание 6: Операции с плавающей точкой (интерактивно)"""
        self.printer.print_section("6. ОПЕРАЦИИ С ПЛАВАЮЩЕЙ ТОЧКОЙ IEEE-754")

        print("Введите два числа с плавающей точкой:")
        num1 = self.get_float_input("Первое число: ")
        num2 = self.get_float_input("Второе число: ")

        print(f"\nЧисло 1: {num1}")
        print(f"Число 2: {num2}")

        # Сложение
        result_bin = self.float_converter.to_binary(num1 + num2)
        self.printer.print_float_operation(f"{num1} + {num2}", num1, num2, result_bin, num1 + num2)

        # Вычитание
        result_bin = self.float_converter.to_binary(num1 - num2)
        self.printer.print_float_operation(f"{num1} - {num2}", num1, num2, result_bin, num1 - num2)

        # Умножение
        result_bin = self.float_converter.to_binary(num1 * num2)
        self.printer.print_float_operation(f"{num1} * {num2}", num1, num2, result_bin, num1 * num2)

        # Деление
        if num2 != 0:
            result_bin = self.float_converter.to_binary(num1 / num2)
            self.printer.print_float_operation(f"{num1} / {num2}", num1, num2, result_bin, num1 / num2)
        else:
            print("Деление на ноль не выполняется")

    def run_task7_interactive(self):
        """Задание 7: 5421 BCD код (интерактивно)"""
        self.printer.print_section("7. 5421 BCD КОД")

        print("Введите два числа для сложения в 5421 BCD коде (0-9999):")
        num1 = self.get_bcd_input("Первое число (0-9999): ")
        num2 = self.get_bcd_input("Второе число (0-9999): ")

        print(f"\nЧисло 1: {num1}")
        print(f"Число 2: {num2}")

        try:
            bcd1 = self.bcd_5421.to_bcd(num1)
            bcd2 = self.bcd_5421.to_bcd(num2)

            self.printer.print_binary(bcd1, f"{num1} в 5421 BCD")
            self.printer.print_binary(bcd2, f"{num2} в 5421 BCD")

            # Сложение
            result_bin, result_dec = self.bcd_5421.add(num1, num2)
            self.printer.print_operation(f"{num1} + {num2}", num1, num2, result_bin, result_dec)

        except ValueError as e:
            print(f"Ошибка: {e}")

    def show_menu(self):
        """Показать меню выбора заданий"""
        print("\n" + "=" * 60)
        print("ВЫБЕРИТЕ ЗАДАНИЕ:")
        print("=" * 60)
        print("1. Перевод чисел в разные коды")
        print("2. Сложение в дополнительном коде")
        print("3. Вычитание через отрицание")
        print("4. Умножение в прямом коде")
        print("5. Деление в прямом коде")
        print("6. Операции с плавающей точкой IEEE-754")
        print("7. 5421 BCD код")
        print("8. ВСЕ ЗАДАНИЯ (с тестовыми данными)")
        print("0. Выход")
        print("=" * 60)

    def run_all_demo(self):
        """Запуск всех заданий с тестовыми данными"""
        self.printer.print_section("ДЕМОНСТРАЦИЯ ВСЕХ ЗАДАНИЙ С ТЕСТОВЫМИ ДАННЫМИ")

        test_numbers = [45, -23, 127, -128]
        a, b = 45, -23
        c, d = 20, 80
        f1, f2 = 12.5, 3.75
        bcd1, bcd2 = 123, 456

        self.run_task1(test_numbers[:2])
        self.run_task2(a, b)
        self.run_task3(a, b)
        self.run_task4(c, d)
        self.run_task5(c, d)
        self.run_task6(f1, f2)
        self.run_task7(bcd1, bcd2)

    def run(self):
        """Главный метод запуска"""
        while True:
            self.show_menu()
            choice = input("Ваш выбор: ").strip()

            if choice == '1':
                self.run_task1_interactive()
            elif choice == '2':
                self.run_task2_interactive()
            elif choice == '3':
                self.run_task3_interactive()
            elif choice == '4':
                self.run_task4_interactive()
            elif choice == '5':
                self.run_task5_interactive()
            elif choice == '6':
                self.run_task6_interactive()
            elif choice == '7':
                self.run_task7_interactive()
            elif choice == '8':
                self.run_all_demo()
            elif choice == '0':
                print("\nДо свидания!")
                break
            else:
                print("\nНеверный выбор. Пожалуйста, выберите 0-8.")

            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    lab = BinaryArithmeticLab()
    lab.run()


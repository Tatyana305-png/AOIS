class BinaryPrinter:
    """Класс для вывода двоичных представлений"""

    def __init__(self):
        self.default_group_size = 8

    def print_binary(self, bits_array, title="", group_size=None):
        """Вывод двоичного представления с группировкой"""
        if group_size is None:
            group_size = self.default_group_size

        if title:
            print(f"{title}: ", end="")

        result = []
        for i in range(0, len(bits_array), group_size):
            group = bits_array[i:i + group_size]
            result.append(''.join(map(str, group)))

        print(' '.join(result))

    def print_section(self, title):
        """Вывод заголовка секции"""
        print("\n" + "=" * 60)
        print(f"{title:^60}")
        print("=" * 60)

    def print_operation(self, operation_name, num1, num2, result_bin, result_dec):
        """Вывод результатов операции"""
        print(f"\n{operation_name}: {num1} и {num2}")
        self.print_binary(result_bin, "Результат в двоичном виде")
        print(f"Результат в десятичном виде: {result_dec}")

    def print_number_conversion(self, num, direct, reverse, additional):
        """Вывод результатов преобразования числа в разные коды"""
        print(f"\nЧисло: {num}")
        self.print_binary(direct, "Прямой код")
        self.print_binary(reverse, "Обратный код")
        self.print_binary(additional, "Дополнительный код")

    def print_float_operation(self, operation_name, num1, num2, result_bin, result):
        """Вывод операции с плавающей точкой"""
        self.print_binary(result_bin, f"{operation_name} (IEEE-754)")
        print(f"Результат: {result}")
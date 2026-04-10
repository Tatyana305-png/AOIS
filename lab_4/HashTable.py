import math
from Record import Record
from Node import Node


class HashTable:
    """Класс хеш-таблицы с разрешением коллизий через связный список"""

    def __init__(self, size=20, start_address=0):
        """
        Инициализация хеш-таблицы

        Args:
            size: размер таблицы (количество строк)
            start_address: начальный адрес таблицы (B)
        """
        self.size = size
        self.start_address = start_address
        self.table = [None] * size
        self.records = []
        self.occupied_count = 0

        self.russian_alphabet = {
            'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ё': 6,
            'Ж': 7, 'З': 8, 'И': 9, 'Й': 10, 'К': 11, 'Л': 12, 'М': 13,
            'Н': 14, 'О': 15, 'П': 16, 'Р': 17, 'С': 18, 'Т': 19, 'У': 20,
            'Ф': 21, 'Х': 22, 'Ц': 23, 'Ч': 24, 'Ш': 25, 'Щ': 26, 'Ъ': 27,
            'Ы': 28, 'Ь': 29, 'Э': 30, 'Ю': 31, 'Я': 32
        }

    def key_to_number(self, key_word):
        """
        Перевод ключевого слова в числовое значение V
        Используются первые две буквы слова (русский алфавит)
        V = a1 * 33^1 + a2 * 33^0

        Args:
            key_word: ключевое слово (строка)

        Returns:
            числовое значение V
        """
        if not key_word:
            return 0

        word_upper = key_word.upper()

        first_char = word_upper[0] if len(word_upper) > 0 else 'А'
        second_char = word_upper[1] if len(word_upper) > 1 else first_char

        v1 = self.russian_alphabet.get(first_char, 0)
        v2 = self.russian_alphabet.get(second_char, 0)

        v = v1 * 33 + v2

        return v

    def hash_function(self, v):
        """
        Функция хеширования: h(V) = V mod H + B

        Args:
            v: числовое значение ключевого слова

        Returns:
            хеш-адрес
        """
        return (v % self.size) + self.start_address

    def insert(self, key_id, key_word, data):
        """
        Вставка записи в хеш-таблицу

        Args:
            key_id: идентификатор ключевого слова
            key_word: ключевое слово
            data: данные

        Returns:
            bool: успешность вставки
        """
        if self.search(key_word):
            print(f"Ошибка: ключевое слово '{key_word}' уже существует в таблице")
            return False

        v = self.key_to_number(key_word)
        h = self.hash_function(v)

        record = Record(key_id, data, key_word)

        if self.table[h] is not None:
            record.c_flag = 1
            print(f"Коллизия для ключа '{key_word}' (V={v}, h={h})")

            current = self.table[h]
            while current.next:
                current = current.next
            current.next = Node(record, len(self.records))
            current.record.t_flag = 0
        else:
            self.table[h] = Node(record, len(self.records))

        self.records.append(record)
        self.occupied_count += 1

        print(f"Добавлена запись: {key_id} -> '{key_word}' (V={v}, h={h})")
        return True

    def search(self, key_word):
        """
        Поиск записи по ключевому слову

        Args:
            key_word: ключевое слово для поиска

        Returns:
            Record: найденная запись или None
        """
        if not key_word:
            return None

        v = self.key_to_number(key_word)
        h = self.hash_function(v)

        current = self.table[h]
        while current:
            record = current.record
            if record.is_occupied() and record.key_word == key_word:
                return record
            current = current.next

        return None

    def delete(self, key_word):
        """
        Удаление записи по ключевому слову

        Args:
            key_word: ключевое слово для удаления

        Returns:
            bool: успешность удаления
        """
        if not key_word:
            return False

        v = self.key_to_number(key_word)
        h = self.hash_function(v)

        prev = None
        current = self.table[h]

        while current:
            record = current.record
            if record.is_occupied() and record.key_word == key_word:
                record.mark_deleted()
                self.occupied_count -= 1

                if prev is None and current.next is None:
                    self.table[h] = None
                elif prev is None:
                    self.table[h] = current.next
                    if self.table[h]:
                        self.table[h].record.t_flag = 1
                else:
                    prev.next = current.next
                    if prev.next is None:
                        prev.record.t_flag = 1

                print(f"Удалена запись с ключевым словом '{key_word}'")
                return True

            prev = current
            current = current.next

        print(f"Запись с ключевым словом '{key_word}' не найдена")
        return False

    def update(self, key_word, new_data):
        """
        Обновление данных записи

        Args:
            key_word: ключевое слово
            new_data: новые данные

        Returns:
            bool: успешность обновления
        """
        record = self.search(key_word)
        if record:
            record.data = new_data
            print(f"Обновлена запись с ключевым словом '{key_word}'")
            return True

        print(f"Запись с ключевым словом '{key_word}' не найдена")
        return False

    def get_fill_factor(self):
        """
        Расчет коэффициента заполнения хеш-таблицы

        Returns:
            float: коэффициент заполнения
        """
        return self.occupied_count / self.size

    def display(self):
        """
        Вывод содержимого хеш-таблицы на экран
        """
        print("\n" + "=" * 120)
        print("ХЕШ-ТАБЛИЦА".center(120))
        print("=" * 120)

        headers = ["№", "ID", "C", "U", "T", "L", "D", "Po", "Pi (данные)"]
        col_widths = [4, 15, 3, 3, 3, 3, 3, 5, 70]

        header_line = ""
        for i, header in enumerate(headers):
            header_line += f"{header:^{col_widths[i]}}|"
        print(header_line)
        print("-" * 120)

        for i in range(self.size):
            row_data = [str(i), "", "", "", "", "", "", "", ""]

            current = self.table[i]
            if current:
                record = current.record
                row_data[1] = record.key_word or record.key_id
                row_data[2] = str(record.c_flag)
                row_data[3] = str(record.u_flag if not record.is_deleted() else 0)
                row_data[4] = str(record.t_flag)
                row_data[5] = str(record.l_flag)
                row_data[6] = str(record.d_flag)
                row_data[7] = str(current.next.index if current.next else "")
                row_data[8] = record.data[:67] + "..." if len(record.data) > 67 else record.data

                line = ""
                for j, val in enumerate(row_data):
                    line += f"{str(val):<{col_widths[j]}}|"
                print(line)

                current = current.next
                while current:
                    record = current.record
                    row_data = ["", "", "", "", "", "", "", "", ""]
                    row_data[1] = f"  └─ {record.key_word or record.key_id}"
                    row_data[2] = str(record.c_flag)
                    row_data[3] = str(record.u_flag if not record.is_deleted() else 0)
                    row_data[4] = str(record.t_flag)
                    row_data[5] = str(record.l_flag)
                    row_data[6] = str(record.d_flag)
                    row_data[7] = str(current.next.index if current.next else "")
                    row_data[8] = record.data[:67] + "..." if len(record.data) > 67 else record.data

                    line = ""
                    for j, val in enumerate(row_data):
                        line += f"{str(val):<{col_widths[j]}}|"
                    print(line)

                    current = current.next
            else:
                line = ""
                for j, val in enumerate(row_data):
                    line += f"{str(val):<{col_widths[j]}}|"
                print(line)

        print("-" * 120)
        print(f"Коэффициент заполнения таблицы: {self.get_fill_factor():.2f} ({self.occupied_count}/{self.size})")
        print("=" * 120)

    def display_all_records_info(self):
        """
        Вывод информации о строках хеш-таблицы
        """
        print("\n" + "=" * 80)
        print("ХЕШ-ТАБЛИЦА (20 СТРОК)".center(80))
        print("=" * 80)
        print(
            f"{'№ строки':<10} {'ID':<15} {'Ключевое слово':<20} {'V (числовое значение)':<25} {'h (хеш-адрес)':<15} {'Статус':<10}")
        print("-" * 95)

        records_by_hash = {}
        for i in range(self.size):
            records_by_hash[i] = []

        for record in self.records:
            if record.key_word and not record.is_deleted():
                v = self.key_to_number(record.key_word)
                h = self.hash_function(v)
                records_by_hash[h].append((record, v))

        for row_num in range(self.size):
            if records_by_hash[row_num]:
                for idx, (record, v) in enumerate(records_by_hash[row_num]):
                    if idx == 0:
                        status = "Активна"
                        print(
                            f"{row_num:<10} {record.key_id:<15} {record.key_word:<20} {v:<25} {row_num:<15} {status:<10}")
                    else:
                        status = f"Коллизия {idx}"
                        print(
                            f"{'':<10} {record.key_id:<15} └─ {record.key_word:<18} {v:<25} {row_num:<15} {status:<10}")
            else:
                print(f"{row_num:<10} {'None':<15} {'None':<20} {'None':<25} {'None':<15} {'Пусто':<10}")

        print("=" * 95)

        print(f"\n ")
        print(f"   Всего строк в таблице: {self.size}")
        print(f"   Занято строк (с данными): {self.occupied_count}")
        print(f"   Пустых строк: {self.size - self.occupied_count}")
        print(f"   Коэффициент заполнения: {self.get_fill_factor():.2f} ({self.occupied_count}/{self.size})")

        collision_count = 0
        for record in self.records:
            if record.c_flag == 1 and not record.is_deleted():
                collision_count += 1
        print(f"   Количество коллизий: {collision_count}")
        print("=" * 95)
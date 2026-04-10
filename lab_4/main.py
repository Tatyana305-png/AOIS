#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Хеш-таблицы
Вариант 1: Разрешение коллизий с помощью цепочек (связный список)
"""

from HashTable import HashTable
from utils import print_menu, get_user_input, clear_screen, init_geography_data


def main():
    """Главная функция программы"""

    hash_table = HashTable(size=20, start_address=0)

    init_geography_data(hash_table)

    while True:
        print_menu()
        choice = get_user_input("\nВыберите действие (0-7): ")

        if choice == '0':
            print("\nВыход из программы. До свидания!")
            break

        elif choice == '1':
            clear_screen()
            hash_table.display()
            input("\nНажмите Enter для продолжения...")

        elif choice == '2':
            clear_screen()
            print("\n--- ДОБАВЛЕНИЕ НОВОЙ ЗАПИСИ ---")
            key_id = get_user_input("Введите ID (например, ID14): ")
            key_word = get_user_input("Введите ключевое слово (географическое название): ")
            data = get_user_input("Введите описание/определение: ")

            if key_id and key_word and data:
                hash_table.insert(key_id, key_word, data)
            else:
                print("Ошибка: все поля должны быть заполнены!")

            input("\nНажмите Enter для продолжения...")

        elif choice == '3':
            clear_screen()
            print("\n--- ПОИСК ЗАПИСИ ---")
            key_word = get_user_input("Введите ключевое слово для поиска: ")

            if key_word:
                record = hash_table.search(key_word)
                if record:
                    print(f"\nЗапись найдена:")
                    print(f"  ID: {record.key_id}")
                    print(f"  Ключевое слово: {record.key_word}")
                    print(f"  Данные: {record.data}")
                    print(
                        f"  Флажки: C={record.c_flag}, U={record.u_flag}, T={record.t_flag}, L={record.l_flag}, D={record.d_flag}")

                    v = hash_table.key_to_number(key_word)
                    h = hash_table.hash_function(v)
                    print(f"  Числовое значение V: {v}")
                    print(f"  Хеш-адрес h: {h}")
                else:
                    print(f"Запись с ключевым словом '{key_word}' не найдена")
            else:
                print("Ошибка: ключевое слово не может быть пустым!")

            input("\nНажмите Enter для продолжения...")

        elif choice == '4':
            clear_screen()
            print("\n--- ОБНОВЛЕНИЕ ЗАПИСИ ---")
            key_word = get_user_input("Введите ключевое слово для обновления: ")

            if key_word:
                record = hash_table.search(key_word)
                if record:
                    print(f"\nТекущие данные: {record.data}")
                    new_data = get_user_input("Введите новые данные: ")
                    if new_data:
                        hash_table.update(key_word, new_data)
                    else:
                        print("Данные не изменены")
                else:
                    print(f"Запись с ключевым словом '{key_word}' не найдена")
            else:
                print("Ошибка: ключевое слово не может быть пустым!")

            input("\nНажмите Enter для продолжения...")

        elif choice == '5':
            clear_screen()
            print("\n--- УДАЛЕНИЕ ЗАПИСИ ---")
            key_word = get_user_input("Введите ключевое слово для удаления: ")

            if key_word:
                confirm = get_user_input(f"Вы уверены, что хотите удалить '{key_word}'? (y/n): ")
                if confirm.lower() == 'y':
                    hash_table.delete(key_word)
                else:
                    print("Удаление отменено")
            else:
                print("Ошибка: ключевое слово не может быть пустым!")

            input("\nНажмите Enter для продолжения...")

        elif choice == '6':
            clear_screen()
            hash_table.display_all_records_info()
            input("\nНажмите Enter для продолжения...")

        elif choice == '7':
            clear_screen()
            print("\n--- КОЭФФИЦИЕНТ ЗАПОЛНЕНИЯ ---")
            fill_factor = hash_table.get_fill_factor()
            print(f"Коэффициент заполнения: {fill_factor:.2f}")
            print(f"Занято записей: {hash_table.occupied_count}")
            print(f"Общий размер таблицы: {hash_table.size}")
            print(f"Процент заполнения: {fill_factor * 100:.1f}%")
            input("\nНажмите Enter для продолжения...")

        else:
            print("Неверный выбор. Пожалуйста, выберите пункт от 0 до 7.")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()

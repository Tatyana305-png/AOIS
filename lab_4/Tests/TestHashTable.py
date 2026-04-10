#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты для класса HashTable
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from HashTable import HashTable
from Record import Record


class TestHashTable(unittest.TestCase):
    """Тесты для класса HashTable"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.hash_table = HashTable(size=20, start_address=0)

        self.test_data = [
            ("ID1", "Евразия", "Крупнейший материк"),
            ("ID2", "Амазонка", "Самая полноводная река"),
            ("ID3", "Байкал", "Самое глубокое озеро"),
            ("ID4", "Анды", "Длиннейшая горная система"),
            ("ID5", "Сахара", "Крупнейшая пустыня"),
        ]

    def test_initialization(self):
        """Тест инициализации хеш-таблицы"""
        self.assertEqual(self.hash_table.size, 20)
        self.assertEqual(self.hash_table.start_address, 0)
        self.assertEqual(len(self.hash_table.table), 20)
        self.assertEqual(self.hash_table.occupied_count, 0)
        self.assertEqual(len(self.hash_table.records), 0)

    def test_custom_size_initialization(self):
        """Тест инициализации с пользовательским размером"""
        ht = HashTable(size=30, start_address=5)
        self.assertEqual(ht.size, 30)
        self.assertEqual(ht.start_address, 5)
        self.assertEqual(len(ht.table), 30)

    def test_key_to_number_single_word(self):
        """Тест перевода ключевого слова в число (односложные слова)"""
        self.assertEqual(self.hash_table.key_to_number("Евразия"), 167)
        self.assertEqual(self.hash_table.key_to_number("Анды"), 14)
        self.assertEqual(self.hash_table.key_to_number("Нил"), 471)

    def test_key_to_number_two_words(self):
        """Тест перевода ключевого слова в число (многосложные слова)"""
        self.assertEqual(self.hash_table.key_to_number("Гималаи"), 108)
        self.assertEqual(self.hash_table.key_to_number("Гренландия"), 116)

    def test_key_to_number_case_insensitive(self):
        """Тест: регистр букв не влияет на результат"""
        self.assertEqual(
            self.hash_table.key_to_number("евразия"),
            self.hash_table.key_to_number("ЕВРАЗИЯ")
        )
        self.assertEqual(
            self.hash_table.key_to_number("евразия"),
            self.hash_table.key_to_number("Евразия")
        )

    def test_key_to_number_single_letter(self):
        """Тест: слово из одной буквы (используется дважды)"""
        self.assertEqual(self.hash_table.key_to_number("А"), 0)
        self.assertEqual(self.hash_table.key_to_number("Я"), 1088)

    def test_key_to_number_empty_string(self):
        """Тест: пустая строка"""
        self.assertEqual(self.hash_table.key_to_number(""), 0)

    def test_key_to_number_with_yo(self):
        """Тест: слова с буквой Ё"""
        self.assertEqual(self.hash_table.key_to_number("Ёлка"), 210)

    def test_hash_function(self):
        """Тест хеш-функции h(V) = V mod H + B"""
        self.assertEqual(self.hash_table.hash_function(167), 167 % 20)  # 7
        self.assertEqual(self.hash_table.hash_function(14), 14 % 20)  # 14
        self.assertEqual(self.hash_table.hash_function(471), 471 % 20)  # 11
        self.assertEqual(self.hash_table.hash_function(0), 0)
        self.assertEqual(self.hash_table.hash_function(20), 0)
        self.assertEqual(self.hash_table.hash_function(21), 1)

    def test_insert_without_collision(self):
        """Тест вставки без коллизии"""
        result = self.hash_table.insert("ID1", "Евразия", "Крупнейший материк")
        self.assertTrue(result)
        self.assertEqual(self.hash_table.occupied_count, 1)

        record = self.hash_table.search("Евразия")
        self.assertIsNotNone(record)
        self.assertEqual(record.key_word, "Евразия")

    def test_insert_with_collision(self):
        """Тест вставки с коллизией"""
        self.hash_table.insert("ID2", "Амазонка", "Река")
        result = self.hash_table.insert("ID3", "Байкал", "Озеро")

        self.assertTrue(result)
        self.assertEqual(self.hash_table.occupied_count, 2)

        record1 = self.hash_table.search("Амазонка")
        record2 = self.hash_table.search("Байкал")
        self.assertIsNotNone(record1)
        self.assertIsNotNone(record2)

        self.assertEqual(record2.c_flag, 1)

    def test_insert_duplicate_key(self):
        """Тест: запрет вставки дубликата ключевого слова"""
        self.hash_table.insert("ID1", "Евразия", "Описание")
        result = self.hash_table.insert("ID2", "Евразия", "Другое описание")

        self.assertFalse(result)
        self.assertEqual(self.hash_table.occupied_count, 1)

    def test_search_existing_key(self):
        """Тест поиска существующего ключа"""
        self.hash_table.insert("ID1", "Евразия", "Крупнейший материк")

        record = self.hash_table.search("Евразия")
        self.assertIsNotNone(record)
        self.assertEqual(record.key_id, "ID1")
        self.assertEqual(record.data, "Крупнейший материк")

    def test_search_nonexistent_key(self):
        """Тест поиска несуществующего ключа"""
        self.hash_table.insert("ID1", "Евразия", "Описание")

        record = self.hash_table.search("Несуществующее")
        self.assertIsNone(record)

    def test_search_empty_key(self):
        """Тест поиска с пустым ключом"""
        self.assertIsNone(self.hash_table.search(""))
        self.assertIsNone(self.hash_table.search(None))

    def test_search_in_collision_chain(self):
        """Тест поиска в цепочке коллизий"""
        self.hash_table.insert("ID2", "Амазонка", "Река")
        self.hash_table.insert("ID3", "Байкал", "Озеро")  # Коллизия

        record = self.hash_table.search("Байкал")
        self.assertIsNotNone(record)
        self.assertEqual(record.key_word, "Байкал")

    def test_update_existing_record(self):
        """Тест обновления существующей записи"""
        self.hash_table.insert("ID1", "Евразия", "Старое описание")

        result = self.hash_table.update("Евразия", "Новое описание")
        self.assertTrue(result)

        record = self.hash_table.search("Евразия")
        self.assertEqual(record.data, "Новое описание")

    def test_update_nonexistent_record(self):
        """Тест обновления несуществующей записи"""
        result = self.hash_table.update("Несуществующее", "Новые данные")
        self.assertFalse(result)

    def test_delete_existing_record(self):
        """Тест удаления существующей записи"""
        self.hash_table.insert("ID1", "Евразия", "Описание")
        self.assertEqual(self.hash_table.occupied_count, 1)

        result = self.hash_table.delete("Евразия")
        self.assertTrue(result)
        self.assertEqual(self.hash_table.occupied_count, 0)

        record = self.hash_table.search("Евразия")
        self.assertIsNone(record)

    def test_delete_nonexistent_record(self):
        """Тест удаления несуществующей записи"""
        result = self.hash_table.delete("Несуществующее")
        self.assertFalse(result)

    def test_delete_first_in_collision_chain(self):
        """Тест удаления первого элемента в цепочке коллизий"""
        self.hash_table.insert("ID2", "Амазонка", "Река")
        self.hash_table.insert("ID3", "Байкал", "Озеро")

        result = self.hash_table.delete("Амазонка")
        self.assertTrue(result)
        self.assertEqual(self.hash_table.occupied_count, 1)

        record = self.hash_table.search("Байкал")
        self.assertIsNotNone(record)

    def test_delete_last_in_collision_chain(self):
        """Тест удаления последнего элемента в цепочке коллизий"""
        self.hash_table.insert("ID2", "Амазонка", "Река")
        self.hash_table.insert("ID3", "Байкал", "Озеро")

        result = self.hash_table.delete("Байкал")
        self.assertTrue(result)
        self.assertEqual(self.hash_table.occupied_count, 1)

        record = self.hash_table.search("Амазонка")
        self.assertIsNotNone(record)

    def test_delete_middle_in_chain(self):
        """Тест удаления элемента из середины цепочки"""
        self.hash_table.insert("ID4", "Анды", "Горы")
        self.hash_table.insert("ID5", "Сахара", "Пустыня")
        self.hash_table.insert("ID11", "Антарктида", "Материк")


        result = self.hash_table.delete("Сахара")
        self.assertTrue(result)
        self.assertEqual(self.hash_table.occupied_count, 2)


        record1 = self.hash_table.search("Анды")
        record3 = self.hash_table.search("Антарктида")
        self.assertIsNotNone(record1)
        self.assertIsNotNone(record3)

    def test_get_fill_factor(self):
        """Тест коэффициента заполнения"""
        self.assertEqual(self.hash_table.get_fill_factor(), 0.0)

        self.hash_table.insert("ID1", "Евразия", "Описание")
        self.assertEqual(self.hash_table.get_fill_factor(), 0.05)  # 1/20

        for i in range(5):
            self.hash_table.insert(f"ID{i + 2}", f"Тест{i}", "Данные")
        self.assertEqual(self.hash_table.get_fill_factor(), 0.3)  # 6/20

    def test_multiple_collisions(self):
        """Тест множественных коллизий"""
        self.hash_table.insert("ID4", "Анды", "Горы")
        self.hash_table.insert("ID5", "Сахара", "Пустыня")
        self.hash_table.insert("ID11", "Антарктида", "Материк")

        self.assertIsNotNone(self.hash_table.search("Анды"))
        self.assertIsNotNone(self.hash_table.search("Сахара"))
        self.assertIsNotNone(self.hash_table.search("Антарктида"))
        self.assertEqual(self.hash_table.occupied_count, 3)

        andy = self.hash_table.search("Анды")
        sahara = self.hash_table.search("Сахара")
        antarctica = self.hash_table.search("Антарктида")

        self.assertEqual(andy.c_flag, 0)  # Первый - без флага коллизии
        self.assertEqual(sahara.c_flag, 1)  # Второй - с флагом
        self.assertEqual(antarctica.c_flag, 1)  # Третий - с флагом

        self.assertEqual(andy.t_flag, 0)  # Не терминальный
        self.assertEqual(sahara.t_flag, 0)  # Не терминальный
        self.assertEqual(antarctica.t_flag, 1)  # Терминальный

    def test_chain_pointer_after_deletion(self):
        """Тест: указатели в цепочке после удаления"""
        self.hash_table.insert("ID4", "Анды", "Горы")
        self.hash_table.insert("ID5", "Сахара", "Пустыня")
        self.hash_table.insert("ID11", "Антарктида", "Материк")

        self.hash_table.delete("Сахара")

        self.assertIsNotNone(self.hash_table.search("Анды"))
        self.assertIsNotNone(self.hash_table.search("Антарктида"))

    def test_display_methods(self):
        """Тест методов отображения (просто проверяем, что не падают)"""
        self.hash_table.insert("ID1", "Евразия", "Описание")

        try:
            self.hash_table.display()
            self.hash_table.display_all_records_info()
        except Exception as e:
            self.fail(f"Метод display упал с ошибкой: {e}")

    def test_large_table(self):
        """Тест работы с большим количеством записей"""
        for i in range(25):
            self.hash_table.insert(f"ID{i}", f"Слово{i}", f"Данные{i}")

        self.assertGreater(self.hash_table.occupied_count, 0)

        for i in range(10):
            record = self.hash_table.search(f"Слово{i}")
            self.assertIsNotNone(record)


if __name__ == '__main__':
    unittest.main()
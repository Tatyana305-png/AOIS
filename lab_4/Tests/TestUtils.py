#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты для вспомогательных функций utils
"""

import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import clear_screen, print_menu, get_user_input, init_geography_data
from HashTable import HashTable


class TestUtils(unittest.TestCase):
    """Тесты для вспомогательных функций"""

    def test_clear_screen(self):
        """Тест очистки экрана (просто проверяем, что не падает)"""
        try:
            clear_screen()
        except Exception as e:
            self.fail(f"clear_screen упал с ошибкой: {e}")

    def test_print_menu(self):
        """Тест вывода меню (просто проверяем, что не падает)"""
        try:
            print_menu()
        except Exception as e:
            self.fail(f"print_menu упал с ошибкой: {e}")

    @patch('builtins.input', return_value='test_input')
    def test_get_user_input_with_input(self, mock_input):
        """Тест получения пользовательского ввода"""
        result = get_user_input("Введите: ")
        self.assertEqual(result, "test_input")

    @patch('builtins.input', return_value='')
    def test_get_user_input_with_default(self, mock_input):
        """Тест получения ввода со значением по умолчанию"""
        result = get_user_input("Введите: ", "default_value")
        self.assertEqual(result, "default_value")

    @patch('builtins.input', return_value='')
    def test_get_user_input_empty_no_default(self, mock_input):
        """Тест: пустой ввод без значения по умолчанию"""
        result = get_user_input("Введите: ")
        self.assertEqual(result, "")

    def test_init_geography_data(self):
        """Тест инициализации географических данных"""
        hash_table = HashTable(size=20)

        captured_output = StringIO()
        sys.stdout = captured_output

        init_geography_data(hash_table)

        sys.stdout = sys.__stdout__

        self.assertGreater(hash_table.occupied_count, 0)

        evrasia = hash_table.search("Евразия")
        self.assertIsNotNone(evrasia)
        self.assertEqual(evrasia.key_id, "ID1")

        amazonka = hash_table.search("Амазонка")
        self.assertIsNotNone(amazonka)
        self.assertEqual(amazonka.key_id, "ID2")

        baikal = hash_table.search("Байкал")
        self.assertIsNotNone(baikal)
        self.assertEqual(baikal.key_id, "ID3")

    def test_init_geography_data_count(self):
        """Тест: количество загруженных записей"""
        hash_table = HashTable(size=20)
        init_geography_data(hash_table)

        self.assertEqual(hash_table.occupied_count, 13)

    def test_init_geography_data_collisions(self):
        """Тест: наличие коллизий в географических данных"""
        hash_table = HashTable(size=20)
        init_geography_data(hash_table)

        has_collision = False
        for record in hash_table.records:
            if record.c_flag == 1 and record.is_occupied():
                has_collision = True
                break

        self.assertTrue(has_collision, "В данных должны быть коллизии")

    def test_init_geography_data_specific_values(self):
        """Тест: проверка конкретных значений V и h"""
        hash_table = HashTable(size=20)
        init_geography_data(hash_table)

        self.assertEqual(hash_table.key_to_number("Евразия"), 167)
        self.assertEqual(hash_table.hash_function(167), 7)

        self.assertEqual(hash_table.key_to_number("Амазонка"), 13)
        self.assertEqual(hash_table.hash_function(13), 13)

        self.assertEqual(hash_table.key_to_number("Байкал"), 33)
        self.assertEqual(hash_table.hash_function(33), 13)

        self.assertEqual(hash_table.key_to_number("Анды"), 14)
        self.assertEqual(hash_table.hash_function(14), 14)

        self.assertEqual(hash_table.key_to_number("Сахара"), 594)
        self.assertEqual(hash_table.hash_function(594), 14)


if __name__ == '__main__':
    unittest.main()
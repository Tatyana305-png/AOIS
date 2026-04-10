#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты для класса Record
"""

import unittest
import sys
import os

# Добавляем родительскую директорию в путь для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Record import Record


class TestRecord(unittest.TestCase):
    """Тесты для класса Record"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.record = Record("ID1", "Крупнейший материк", "Евразия")

    def test_record_initialization(self):
        """Тест инициализации записи"""
        self.assertEqual(self.record.key_id, "ID1")
        self.assertEqual(self.record.key_word, "Евразия")
        self.assertEqual(self.record.data, "Крупнейший материк")
        self.assertEqual(self.record.c_flag, 0)
        self.assertEqual(self.record.u_flag, 1)
        self.assertEqual(self.record.t_flag, 1)
        self.assertEqual(self.record.l_flag, 0)
        self.assertEqual(self.record.d_flag, 0)
        self.assertEqual(self.record.po, -1)

    def test_record_without_key_word(self):
        """Тест записи без ключевого слова"""
        record = Record("ID2", "Описание")
        self.assertEqual(record.key_id, "ID2")
        self.assertEqual(record.key_word, None)
        self.assertEqual(record.data, "Описание")

    def test_mark_deleted(self):
        """Тест пометки записи как удаленной"""
        self.record.mark_deleted()
        self.assertEqual(self.record.d_flag, 1)
        self.assertEqual(self.record.u_flag, 0)

    def test_is_deleted(self):
        """Тест проверки статуса удаления"""
        self.assertFalse(self.record.is_deleted())
        self.record.mark_deleted()
        self.assertTrue(self.record.is_deleted())

    def test_is_occupied(self):
        """Тест проверки занятости записи"""
        self.assertTrue(self.record.is_occupied())
        self.record.mark_deleted()
        self.assertFalse(self.record.is_occupied())

    def test_is_occupied_with_u_flag_zero(self):
        """Тест: запись не занята, если U=0"""
        self.record.u_flag = 0
        self.assertFalse(self.record.is_occupied())

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        expected = {
            'ID': 'Евразия',
            'C': 0,
            'U': 1,
            'T': 1,
            'L': 0,
            'D': 0,
            'Po': '',
            'Pi': 'Крупнейший материк'
        }
        self.assertEqual(self.record.to_dict(), expected)

    def test_to_dict_without_key_word(self):
        """Тест преобразования в словарь без ключевого слова"""
        record = Record("ID2", "Данные")
        expected = {
            'ID': 'ID2',
            'C': 0,
            'U': 1,
            'T': 1,
            'L': 0,
            'D': 0,
            'Po': '',
            'Pi': 'Данные'
        }
        self.assertEqual(record.to_dict(), expected)

    def test_to_dict_with_po(self):
        """Тест преобразования в словарь с указателем Po"""
        self.record.po = 5
        result = self.record.to_dict()
        self.assertEqual(result['Po'], 5)

    def test_string_representation(self):
        """Тест строкового представления"""
        result = str(self.record)
        # Исправлено: теперь проверяем key_id, который есть в строковом представлении
        self.assertIn("ID1", result)
        self.assertIn("Крупнейший материк", result)
        self.assertIn("C=0", result)
        self.assertIn("U=1", result)

    def test_flags_modification(self):
        """Тест изменения флажков"""
        self.record.c_flag = 1
        self.record.t_flag = 0
        self.record.l_flag = 1

        self.assertEqual(self.record.c_flag, 1)
        self.assertEqual(self.record.t_flag, 0)
        self.assertEqual(self.record.l_flag, 1)

    def test_po_modification(self):
        """Тест изменения указателя Po"""
        self.record.po = 10
        self.assertEqual(self.record.po, 10)

        self.record.po = -1
        self.assertEqual(self.record.po, -1)

    def test_data_modification(self):
        """Тест изменения данных"""
        self.record.data = "Новое описание"
        self.assertEqual(self.record.data, "Новое описание")

    # Дополнительные тесты для полноты покрытия

    def test_deleted_record_not_occupied(self):
        """Тест: удаленная запись не считается занятой"""
        self.record.mark_deleted()
        self.assertFalse(self.record.is_occupied())

    def test_multiple_flag_changes(self):
        """Тест множественных изменений флажков"""
        self.record.c_flag = 1
        self.record.t_flag = 0
        self.record.mark_deleted()

        self.assertEqual(self.record.c_flag, 1)
        self.assertEqual(self.record.t_flag, 0)
        self.assertTrue(self.record.is_deleted())

    def test_empty_data(self):
        """Тест с пустыми данными"""
        record = Record("ID3", "")
        self.assertEqual(record.data, "")
        self.assertIsNotNone(record.to_dict())


if __name__ == '__main__':
    unittest.main()
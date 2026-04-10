#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты для класса Node
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Record import Record
from Node import Node


class TestNode(unittest.TestCase):
    """Тесты для класса Node"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.record = Record("ID1", "Тестовые данные", "Тест")
        self.node = Node(self.record, 0)

    def test_node_initialization(self):
        """Тест инициализации узла"""
        self.assertEqual(self.node.record, self.record)
        self.assertEqual(self.node.index, 0)
        self.assertIsNone(self.node.next)

    def test_node_with_different_index(self):
        """Тест узла с разными индексами"""
        node2 = Node(self.record, 15)
        self.assertEqual(node2.index, 15)

    def test_node_next_reference(self):
        """Тест ссылки на следующий узел"""
        record2 = Record("ID2", "Другие данные", "Тест2")
        node2 = Node(record2, 1)

        self.node.next = node2
        self.assertEqual(self.node.next, node2)
        self.assertEqual(self.node.next.record, record2)
        self.assertEqual(self.node.next.index, 1)

    def test_node_chain(self):
        """Тест цепочки узлов"""
        record2 = Record("ID2", "Данные 2", "Тест2")
        record3 = Record("ID3", "Данные 3", "Тест3")

        node1 = Node(self.record, 0)
        node2 = Node(record2, 1)
        node3 = Node(record3, 2)

        node1.next = node2
        node2.next = node3

        self.assertEqual(node1.next, node2)
        self.assertEqual(node1.next.next, node3)
        self.assertIsNone(node3.next)

    def test_string_representation(self):
        """Тест строкового представления"""
        result = str(self.node)
        self.assertIn("Node(index=0", result)
        self.assertIn("record=ID1", result)

    def test_node_with_deleted_record(self):
        """Тест узла с удаленной записью"""
        self.record.mark_deleted()
        node = Node(self.record, 0)
        self.assertTrue(node.record.is_deleted())

    def test_multiple_nodes_same_record(self):
        """Тест: несколько узлов могут ссылаться на одну запись"""
        node1 = Node(self.record, 0)
        node2 = Node(self.record, 1)

        self.assertEqual(node1.record, node2.record)
        self.assertNotEqual(node1.index, node2.index)


if __name__ == '__main__':
    unittest.main()
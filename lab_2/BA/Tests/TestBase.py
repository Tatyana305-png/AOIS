import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class BaseTestCase(unittest.TestCase):
    """Базовый класс для всех тестов"""

    @classmethod
    def setUpClass(cls):
        """Настройка перед всеми тестами класса"""
        pass

    @classmethod
    def tearDownClass(cls):
        """Очистка после всех тестов класса"""
        pass

    def setUp(self):
        """Настройка перед каждым тестом"""
        pass

    def tearDown(self):
        """Очистка после каждого теста"""
        pass
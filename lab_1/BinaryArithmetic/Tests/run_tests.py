#!/usr/bin/env python3
"""
Скрипт для запуска всех тестов проекта
"""

import unittest
import sys
import os


def run_all_tests():
    """Запуск всех тестов"""
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_specific_tests(test_path):
    """Запуск конкретного теста или пакета тестов"""
    loader = unittest.TestLoader()

    if os.path.isfile(test_path):
        suite = loader.discover(os.path.dirname(test_path),
                                pattern=os.path.basename(test_path))
    else:
        suite = loader.discover(test_path, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("ЗАПУСК ТЕСТОВ ПРОЕКТА")
    print("=" * 70)

    if len(sys.argv) > 1:
        test_path = sys.argv[1]
        success = run_specific_tests(test_path)
    else:
        success = run_all_tests()

    print("\n" + "=" * 70)
    if success:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
    print("=" * 70)

    sys.exit(0 if success else 1)
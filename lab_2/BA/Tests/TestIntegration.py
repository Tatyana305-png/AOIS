import sys
import os
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Main import BooleanFunctionAnalyzer
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser


class TestIntegration(BaseTestCase):
    """Интеграционные тесты"""

    def setUp(self):
        super().setUp()
        self.analyzer = BooleanFunctionAnalyzer()
        self.parser = BooleanExpressionParser()

    def test_analyzer_creation(self):
        """Тест создания анализатора"""
        self.assertIsNotNone(self.analyzer)

    def test_analyze_and_function(self):
        """Тест анализа функции AND"""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.analyzer.analyze("a&b")

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertTrue("a&b" in output)
        self.assertTrue("ТАБЛИЦА ИСТИННОСТИ" in output)

    def test_analyze_or_function(self):
        """Тест анализа функции OR"""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.analyzer.analyze("a|b")

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertTrue("a|b" in output)

    def test_analyze_complex_function(self):
        """Тест анализа сложной функции"""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.analyzer.analyze("!(!a->!b)|c")

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertTrue("!(!a->!b)|c" in output)

    def test_analyze_invalid_function(self):
        """Тест анализа некорректной функции"""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.analyzer.analyze("a&")

        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertTrue("Ошибка" in output)

    def test_full_pipeline(self):
        """Тест полного конвейера обработки"""
        expr = "a&b"
        f = BooleanFunction(expr, self.parser)

        self.assertEqual(f.expression, expr)
        self.assertEqual(len(f.variables), 2)
        self.assertEqual(len(f.truth_table), 4)

    def test_multiple_analyses(self):
        """Тест множественного анализа"""
        expressions = ["a&b", "a|b", "!a", "a->b", "a~b"]

        for expr in expressions:
            try:
                self.analyzer.analyze(expr)
            except Exception as e:
                self.fail(f"Analysis failed for {expr}: {e}")
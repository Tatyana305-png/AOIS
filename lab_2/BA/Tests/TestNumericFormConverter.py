from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser
from BooleanAnalyzer.Services.NumericFormConverter import NumericFormConverter


class TestNumericFormConverter(BaseTestCase):
    """Тесты конвертера числовых форм"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()
        self.converter = NumericFormConverter()

    def test_numeric_forms_and(self):
        """Тест числовых форм для AND"""
        f = BooleanFunction("a&b", self.parser)
        sdnf_num, sknf_num = self.converter.convert(f)
        self.assertEqual(sdnf_num, '∨(3)')
        self.assertEqual(sknf_num, '∧(0,1,2)')

    def test_numeric_forms_or(self):
        """Тест числовых форм для OR"""
        f = BooleanFunction("a|b", self.parser)
        sdnf_num, sknf_num = self.converter.convert(f)
        self.assertEqual(sdnf_num, '∨(1,2,3)')
        self.assertEqual(sknf_num, '∧(0)')

    def test_numeric_forms_not(self):
        """Тест числовых форм для NOT"""
        f = BooleanFunction("!a", self.parser)
        sdnf_num, sknf_num = self.converter.convert(f)
        self.assertEqual(sdnf_num, '∨(0)')
        self.assertEqual(sknf_num, '∧(1)')

    def test_numeric_forms_implication(self):
        """Тест числовых форм для импликации"""
        f = BooleanFunction("a->b", self.parser)
        sdnf_num, sknf_num = self.converter.convert(f)
        self.assertEqual(sdnf_num, '∨(0,1,3)')
        self.assertEqual(sknf_num, '∧(2)')

    def test_numeric_forms_equivalence(self):
        """Тест числовых форм для эквивалентности"""
        f = BooleanFunction("a~b", self.parser)
        sdnf_num, sknf_num = self.converter.convert(f)
        self.assertEqual(sdnf_num, '∨(0,3)')
        self.assertEqual(sknf_num, '∧(1,2)')

    def test_index_form_and(self):
        """Тест индексной формы для AND"""
        f = BooleanFunction("a&b", self.parser)
        index = self.converter.get_index_form(f)
        self.assertTrue('8' in index or '1000' in index)

    def test_index_form_or(self):
        """Тест индексной формы для OR"""
        f = BooleanFunction("a|b", self.parser)
        index = self.converter.get_index_form(f)
        self.assertTrue('14' in index or '1110' in index)

    def test_index_form_not(self):
        """Тест индексной формы для NOT"""
        f = BooleanFunction("!a", self.parser)
        index = self.converter.get_index_form(f)
        self.assertTrue('1' in index or '01' in index)

    def test_index_form_complex(self):
        """Тест индексной формы для сложной функции"""
        f = BooleanFunction("!(!a->!b)|c", self.parser)
        index = self.converter.get_index_form(f)
        self.assertTrue(isinstance(index, str))
        self.assertTrue(len(index) > 0)
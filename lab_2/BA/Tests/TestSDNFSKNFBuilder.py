import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tests.TestBase import BaseTestCase
from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser
from BooleanAnalyzer.Services.SDNFSKNFBuilder import StandardFormBuilder
from BooleanAnalyzer.Utils.TermParser import TermParser


class TestSDNFSKNFBuilder(BaseTestCase):
    """Тесты построителя СДНФ и СКНФ"""

    def setUp(self):
        super().setUp()
        self.parser = BooleanExpressionParser()
        self.term_parser = TermParser()
        self.builder = StandardFormBuilder(self.term_parser)

    def test_sdnf_and(self):
        """Тест СДНФ для AND"""
        f = BooleanFunction("a&b", self.parser)
        sdnf, _ = self.builder.build(f)
        self.assertTrue('a&b' in sdnf.replace(' ', ''))

    def test_sknf_and(self):
        """Тест СКНФ для AND"""
        f = BooleanFunction("a&b", self.parser)
        _, sknf = self.builder.build(f)
        self.assertTrue(len(sknf) > 0)

    def test_sdnf_or(self):
        """Тест СДНФ для OR"""
        f = BooleanFunction("a|b", self.parser)
        sdnf, _ = self.builder.build(f)
        terms = sdnf.split(' ∨ ')
        self.assertEqual(len(terms), 3)

    def test_sknf_or(self):
        """Тест СКНФ для OR"""
        f = BooleanFunction("a|b", self.parser)
        _, sknf = self.builder.build(f)
        # СКНФ для OR: (a|b)
        self.assertTrue('a|b' in sknf or 'b|a' in sknf)

    def test_sdnf_not(self):
        """Тест СДНФ для NOT"""
        f = BooleanFunction("!a", self.parser)
        sdnf, _ = self.builder.build(f)
        self.assertTrue('!a' in sdnf)

    def test_sknf_not(self):
        """Тест СКНФ для NOT"""
        f = BooleanFunction("!a", self.parser)
        _, sknf = self.builder.build(f)
        self.assertTrue('a' in sknf or '!a' in sknf)

    def test_sdnf_tautology(self):
        """Тест СДНФ для тавтологии"""
        f = BooleanFunction("a|!a", self.parser)
        sdnf, _ = self.builder.build(f)
        self.assertNotEqual(sdnf, '0')

    def test_sknf_tautology(self):
        """Тест СКНФ для тавтологии"""
        f = BooleanFunction("a|!a", self.parser)
        _, sknf = self.builder.build(f)
        self.assertEqual(sknf, '1')

    def test_sdnf_contradiction(self):
        """Тест СДНФ для противоречия"""
        f = BooleanFunction("a&!a", self.parser)
        sdnf, _ = self.builder.build(f)
        self.assertEqual(sdnf, '0')

    def test_sknf_contradiction(self):
        """Тест СКНФ для противоречия"""
        f = BooleanFunction("a&!a", self.parser)
        _, sknf = self.builder.build(f)
        self.assertNotEqual(sknf, '1')

    def test_format_sdnf_empty(self):
        """Тест форматирования пустой СДНФ"""
        result = self.builder.format_sdnf([])
        self.assertEqual(result, '0')

    def test_format_sknf_empty(self):
        """Тест форматирования пустой СКНФ"""
        result = self.builder.format_sknf([])
        self.assertEqual(result, '1')
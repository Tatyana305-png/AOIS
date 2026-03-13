from typing import Tuple, List
from abc import ABC, abstractmethod
from ..Models.BooleanFunction import BooleanFunction
from ..Utils.TermParser import TermParser


class ISDNFSKNFFormat(ABC):
    """Интерфейс для форматирования СДНФ/СКНФ"""

    @abstractmethod
    def format_sdnf(self, terms: List[str]) -> str:
        pass

    @abstractmethod
    def format_sknf(self, terms: List[str]) -> str:
        pass


class StandardFormBuilder(ISDNFSKNFFormat):
    """Построитель СДНФ и СКНФ"""

    def __init__(self, term_parser: TermParser):
        self.term_parser = term_parser

    def build(self, function: BooleanFunction) -> Tuple[str, str]:
        """Построение СДНФ и СКНФ"""
        sdnf_terms = []
        sknf_terms = []

        for bits, result in function.truth_table:
            if result == 1:
                term = self._bits_to_sdnf_term(bits, function.variables)
                if term:
                    sdnf_terms.append(term)
            else:
                term = self._bits_to_sknf_term(bits, function.variables)
                if term:
                    sknf_terms.append(term)

        sdnf = self.format_sdnf(sdnf_terms)
        sknf = self.format_sknf(sknf_terms)

        return sdnf, sknf

    def _bits_to_sdnf_term(self, bits: Tuple[int, ...], variables: List[str]) -> str:
        """Преобразование набора в терм СДНФ"""
        literals = []
        for var, bit in zip(variables, bits):
            if bit == 1:
                literals.append(var)
            else:
                literals.append(f'!{var}')
        return self.term_parser.join_literals(literals, '&')

    def _bits_to_sknf_term(self, bits: Tuple[int, ...], variables: List[str]) -> str:
        """Преобразование набора в терм СКНФ"""
        literals = []
        for var, bit in zip(variables, bits):
            if bit == 0:
                literals.append(var)
            else:
                literals.append(f'!{var}')
        return self.term_parser.join_literals(literals, '|')

    def format_sdnf(self, terms: List[str]) -> str:
        if not terms:
            return '0'
        unique_terms = sorted(set(terms), key=lambda x: (len(x), x))
        return ' ∨ '.join(unique_terms)

    def format_sknf(self, terms: List[str]) -> str:
        if not terms:
            return '1'
        unique_terms = sorted(set(terms), key=lambda x: (len(x), x))
        return ' ∧ '.join(unique_terms)
from typing import List, Set
import re


class TermParser:
    """Парсер термов логических выражений"""

    def parse_term(self, term: str) -> List[str]:
        """Разбор терма на литералы"""
        term = term.strip('()')
        if '&' in term:
            return term.split('&')
        if '|' in term:
            return term.split('|')
        return [term]

    def parse_dnf(self, dnf: str) -> List[str]:
        """Разбор ДНФ на термы"""
        if '∨' in dnf:
            terms = dnf.split(' ∨ ')
        elif '|' in dnf:
            terms = dnf.split(' | ')
        else:
            terms = [dnf]

        return [t.strip('()') for t in terms]

    def join_literals(self, literals: List[str], operator: str) -> str:
        """Объединение литералов в терм"""
        if not literals:
            return ''
        if len(literals) == 1:
            return literals[0]
        return f'({operator.join(literals)})'

    def get_literal_variable(self, literal: str) -> str:
        """Получение переменной из литерала"""
        return literal.replace('!', '')

    def is_negated(self, literal: str) -> bool:
        """Проверка, является ли литерал отрицанием"""
        return literal.startswith('!')
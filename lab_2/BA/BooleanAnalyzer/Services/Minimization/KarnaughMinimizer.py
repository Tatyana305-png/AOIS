from typing import Tuple, List, Dict, Set
from .BaseMinimizer import BaseMinimizer
from ...Models.BooleanFunction import BooleanFunction


class KarnaughMinimizer(BaseMinimizer):
    """Минимизация табличным методом (карта Карно)"""

    def minimize(self, function: BooleanFunction) -> Tuple[str, str]:
        """Минимизация с использованием карты Карно"""
        n = len(function.variables)

        if n > 4:
            return "Карты Карно поддерживаются только для до 4 переменных", ""

        k_map, map_str = self._build_map(function)

        groups = self._find_groups(k_map, n, function.variables)

        terms = []
        for group in groups:
            term = self._group_to_term(group, function.variables)
            if term:
                terms.append(term)

        if not terms:
            return '0', map_str

        unique_terms = list(set(terms))
        minimized = ' ∨ '.join(unique_terms)
        return minimized, map_str

    def _build_map(self, function: BooleanFunction) -> Tuple[Dict, str]:
        """Построение карты Карно"""
        n = len(function.variables)

        if n == 1:
            return self._build_map_1var(function)
        elif n == 2:
            return self._build_map_2var(function)
        elif n == 3:
            return self._build_map_3var(function)
        else:
            return self._build_map_4var(function)

    def _build_map_1var(self, function: BooleanFunction) -> Tuple[Dict, str]:
        """Карта для 1 переменной"""
        k_map = {}
        map_str = "a\\ 0 1\n"
        map_str += "-" * 10 + "\n"

        for val in [0, 1]:
            for bits, result in function.truth_table:
                if bits[0] == val:
                    k_map[(val,)] = result
                    map_str += f"{val}   {result}\n"

        return k_map, map_str

    def _build_map_2var(self, function: BooleanFunction) -> Tuple[Dict, str]:
        """Карта для 2 переменных (порядок Грея)"""
        k_map = {}
        map_str = "a\\b 0 1\n"
        map_str += "-" * 15 + "\n"

        for a in [0, 1]:
            row = f"{a}   "
            for b in [0, 1]:
                bits = (a, b)
                for tb, res in function.truth_table:
                    if tb == bits:
                        k_map[(a, b)] = res
                        row += f"{res} "
            map_str += row + "\n"

        return k_map, map_str

    def _build_map_3var(self, function: BooleanFunction) -> Tuple[Dict, str]:
        """Карта для 3 переменных (a - строки, bc - столбцы в порядке Грея)"""
        k_map = {}
        map_str = "a\\bc 00 01 11 10\n"
        map_str += "-" * 30 + "\n"

        gray_order = [(0, 0), (0, 1), (1, 1), (1, 0)]

        for a in [0, 1]:
            row = f"{a}    "
            for b, c in gray_order:
                bits = (a, b, c)
                for tb, res in function.truth_table:
                    if tb == bits:
                        k_map[(a, b, c)] = res
                        row += f"{res}  "
            map_str += row + "\n"

        return k_map, map_str

    def _build_map_4var(self, function: BooleanFunction) -> Tuple[Dict, str]:
        """Карта для 4 переменных (ab - строки, cd - столбцы, оба в порядке Грея)"""
        k_map = {}
        map_str = "ab\\cd 00 01 11 10\n"
        map_str += "-" * 35 + "\n"

        gray_order = [(0, 0), (0, 1), (1, 1), (1, 0)]

        for a, b in gray_order:
            row = f"{a}{b}    "
            for c, d in gray_order:
                bits = (a, b, c, d)
                for tb, res in function.truth_table:
                    if tb == bits:
                        k_map[(a, b, c, d)] = res
                        row += f"{res}  "
            map_str += row + "\n"

        return k_map, map_str

    def _find_groups(self, k_map: Dict, n_vars: int, variables: List[str]) -> List[List[Tuple]]:
        """Поиск групп единиц (прямоугольников размером 2^k)"""
        ones = [pos for pos, val in k_map.items() if val == 1]

        if not ones:
            return []

        return [[pos] for pos in ones]

    def _group_to_term(self, group: List[Tuple], variables: List[str]) -> str:
        """Преобразование группы в терм"""
        if not group:
            return ''

        n_vars = len(group[0])
        const_literals = []

        for i in range(n_vars):
            values = set(pos[i] for pos in group)
            if len(values) == 1:
                var = variables[i]
                val = list(values)[0]
                if val == 1:
                    const_literals.append(var)
                else:
                    const_literals.append(f'!{var}')

        if not const_literals:
            return '1'

        if len(const_literals) == 1:
            return const_literals[0]

        return '(' + '&'.join(const_literals) + ')'

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

        groups = self._find_groups(k_map, n)

        terms = []
        for group in groups:
            term = self._group_to_term(group, function.variables)
            if term:
                terms.append(term)

        if not terms:
            return '0', map_str

        minimized = ' ∨ '.join(terms)
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
        else:  # n == 4
            return self._build_map_4var(function)

    def _build_map_1var(self, function: BooleanFunction) -> Tuple[Dict, str]:
        """Карта для 1 переменной"""
        k_map = {}
        map_str = "a\\ 0 1\n"

        for val in [0, 1]:
            for bits, result in function.truth_table:
                if bits[0] == val:
                    k_map[(val,)] = result
                    map_str += f"{val}   {result}\n"

        return k_map, map_str

    def _build_map_2var(self, function: BooleanFunction) -> Tuple[Dict, str]:
        """Карта для 2 переменных"""
        k_map = {}
        map_str = "ab\\ 00 01 11 10\n"

        gray_order = [(0, 0), (0, 1), (1, 1), (1, 0)]

        for a in [0, 1]:
            row = f"{a}   "
            for b_gray in gray_order:
                bits = (a, b_gray[1])
                for tb, res in function.truth_table:
                    if tb == bits:
                        k_map[(a, b_gray[1])] = res
                        row += f"{res} "
            map_str += row + "\n"

        return k_map, map_str

    def _build_map_3var(self, function: BooleanFunction) -> Tuple[Dict, str]:
        """Карта для 3 переменных"""
        k_map = {}
        map_str = "ab\\c 0 1\n"

        for a in [0, 1]:
            for b in [0, 1]:
                row = f"{a}{b}   "
                for c in [0, 1]:
                    bits = (a, b, c)
                    for tb, res in function.truth_table:
                        if tb == bits:
                            k_map[(a, b, c)] = res
                            row += f"{res} "
                map_str += row + "\n"

        return k_map, map_str

    def _build_map_4var(self, function: BooleanFunction) -> Tuple[Dict, str]:
        """Карта для 4 переменных"""
        k_map = {}
        map_str = "ab\\cd 00 01 11 10\n"

        gray_order = [(0, 0), (0, 1), (1, 1), (1, 0)]

        for a in [0, 1]:
            for b in [0, 1]:
                row = f"{a}{b}   "
                for cd in gray_order:
                    bits = (a, b, cd[0], cd[1])
                    for tb, res in function.truth_table:
                        if tb == bits:
                            k_map[(a, b, cd[0], cd[1])] = res
                            row += f"{res} "
                map_str += row + "\n"

        return k_map, map_str

    def _find_groups(self, k_map: Dict, n_vars: int) -> List[List[Tuple]]:
        """Поиск групп единиц"""
        # Упрощенная реализация - каждая единица как группа
        # В реальном проекте здесь должен быть сложный алгоритм поиска прямоугольников
        ones = [pos for pos, val in k_map.items() if val == 1]
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

        return '(' + '&'.join(const_literals) + ')'
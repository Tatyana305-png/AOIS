from typing import List
from ..Models.BooleanFunction import BooleanFunction


class FictitiousVariableFinder:
    """Поиск фиктивных переменных"""

    def find(self, function: BooleanFunction) -> List[str]:
        """Поиск фиктивных переменных"""
        if len(function.variables) <= 1:
            return []

        fictitious = []
        all_vars = set(['a', 'b', 'c', 'd', 'e'])
        present_vars = set(function.variables)

        for var in all_vars - present_vars:
            fictitious.append(var)

        for idx, var in enumerate(function.variables):
            if self._is_fictitious(function, idx):
                fictitious.append(var)

        return sorted(fictitious)

    def _is_fictitious(self, function: BooleanFunction, var_index: int) -> bool:
        """Проверка, является ли переменная фиктивной"""
        for bits, result in function.truth_table:
            opposite_bits = list(bits)
            opposite_bits[var_index] = 1 - opposite_bits[var_index]
            opposite_bits = tuple(opposite_bits)

            try:
                opposite_result = function.truth_table.get_value_at(opposite_bits)
                if result != opposite_result:
                    return False
            except ValueError:
                return False

        return True
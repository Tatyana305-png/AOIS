from typing import Tuple
from ..Models.BooleanFunction import BooleanFunction


class NumericFormConverter:
    """Преобразователь в числовые формы"""

    def convert(self, function: BooleanFunction) -> Tuple[str, str]:
        """Конвертация в числовые формы"""
        sdnf_numbers = function.truth_table.get_ones_indices()
        sknf_numbers = function.truth_table.get_zeros_indices()

        sdnf_form = f"∨({','.join(map(str, sdnf_numbers))})" if sdnf_numbers else "∨()"
        sknf_form = f"∧({','.join(map(str, sknf_numbers))})" if sknf_numbers else "∧()"

        return sdnf_form, sknf_form

    def get_index_form(self, function: BooleanFunction) -> str:
        """Получение индексной формы"""
        results = function.truth_table.get_result_column()
        binary_str = ''.join(map(str, results[::-1]))  # младший разряд - первый набор
        decimal_value = int(binary_str, 2)

        return f"({','.join(map(str, results))})_2 = {decimal_value}_10"
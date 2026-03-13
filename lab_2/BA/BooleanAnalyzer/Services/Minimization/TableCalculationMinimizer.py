from typing import Tuple, List, Dict, Set
from tabulate import tabulate
from .BaseMinimizer import BaseMinimizer
from .CalculationMinimizer import CalculationMinimizer
from ...Models.BooleanFunction import BooleanFunction


class TableCalculationMinimizer(BaseMinimizer):
    """Минимизация расчетно-табличным методом"""

    def __init__(self):
        super().__init__()
        self.calc_minimizer = CalculationMinimizer()

    def minimize(self, function: BooleanFunction) -> Tuple[str, List[str], str]:
        """Минимизация с построением таблицы покрытия"""
        minimized, stages = self.calc_minimizer.minimize(function)

        if minimized == '0' or minimized == '1':
            return minimized, stages, "Таблица покрытия не требуется"

        implicants = self.term_parser.parse_dnf(minimized)
        ones_sets = function.truth_table.get_ones_sets()

        table = self._build_coverage_table(implicants, ones_sets, function.variables)

        return minimized, stages, table

    def _build_coverage_table(self, implicants: List[str],
                              ones_sets: List[Tuple[int, ...]],
                              variables: List[str]) -> str:
        """Построение таблицы покрытия"""
        if not ones_sets:
            return "Нет наборов с результатом 1"

        headers = ['Импликанты'] + [f"{bits}" for bits in ones_sets]
        table_data = []

        for imp in implicants:
            row = [imp]
            for bits in ones_sets:
                if self._term_covers(imp, bits, variables):
                    row.append('X')
                else:
                    row.append('')
            table_data.append(row)

        return tabulate(table_data, headers=headers, tablefmt='grid')
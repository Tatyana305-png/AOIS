from abc import ABC, abstractmethod
from typing import Tuple, List
from ...Models.BooleanFunction import BooleanFunction
from ...Utils.TermParser import TermParser


class BaseMinimizer(ABC):
    """Базовый класс для минимизаторов"""

    def __init__(self):
        self.term_parser = TermParser()

    @abstractmethod
    def minimize(self, function: BooleanFunction) -> Tuple[str, List[str]]:
        """Минимизация функции"""
        pass

    def _get_ones_sets(self, function: BooleanFunction) -> List[Tuple[int, ...]]:
        """Получение наборов, на которых функция равна 1"""
        return function.truth_table.get_ones_sets()

    def _term_covers(self, term: str, bits: Tuple[int, ...],
                     variables: List[str]) -> bool:
        """Проверка, покрывает ли терм набор"""
        literals = self.term_parser.parse_term(term)
        var_dict = dict(zip(variables, bits))

        for lit in literals:
            if lit.startswith('!'):
                var = lit[1:]
                if var_dict[var] != 0:
                    return False
            else:
                if var_dict[lit] != 1:
                    return False
        return True
from typing import Dict, List
from abc import ABC, abstractmethod
from ..Models.BooleanFunction import BooleanFunction


class IPostClassChecker(ABC):
    """Интерфейс для проверки классов Поста"""

    @abstractmethod
    def check_t0(self, function: BooleanFunction) -> bool:
        pass

    @abstractmethod
    def check_t1(self, function: BooleanFunction) -> bool:
        pass

    @abstractmethod
    def check_s(self, function: BooleanFunction) -> bool:
        pass

    @abstractmethod
    def check_m(self, function: BooleanFunction) -> bool:
        pass

    @abstractmethod
    def check_l(self, function: BooleanFunction) -> bool:
        pass


class PostClassChecker(IPostClassChecker):
    """Проверка принадлежности к классам Поста"""

    def check_all(self, function: BooleanFunction) -> Dict[str, bool]:
        """Проверка всех классов"""
        return {
            'T0': self.check_t0(function),
            'T1': self.check_t1(function),
            'S': self.check_s(function),
            'M': self.check_m(function),
            'L': self.check_l(function)
        }

    def check_t0(self, function: BooleanFunction) -> bool:
        """Проверка сохранения 0"""
        if not function.truth_table:
            return False
        first_result = function.truth_table.get_result_column()[0]
        return first_result == 0

    def check_t1(self, function: BooleanFunction) -> bool:
        """Проверка сохранения 1"""
        if not function.truth_table:
            return False
        last_result = function.truth_table.get_result_column()[-1]
        return last_result == 1

    def check_s(self, function: BooleanFunction) -> bool:
        """Проверка самодвойственности"""
        results = function.truth_table.get_result_column()
        n = len(results)

        if len(function.variables) == 0:
            return False

        for i in range(n // 2):
            if results[i] == results[n - 1 - i]:
                return False
        return True

    def check_m(self, function: BooleanFunction) -> bool:
        """Проверка монотонности"""
        if len(function.variables) == 0:
            return True

        n_vars = len(function.variables)
        results = function.truth_table.get_result_column()
        table = list(function.truth_table)

        for i in range(len(table)):
            for j in range(len(table)):
                bits_i = table[i][0]
                bits_j = table[j][0]

                if all(bits_i[k] <= bits_j[k] for k in range(n_vars)):
                    if results[i] > results[j]:
                        return False
        return True

    def check_l(self, function: BooleanFunction) -> bool:
        """Проверка линейности"""
        if len(function.variables) == 0:
            return True

        from ..Services.ZhegalkinPolynomialBuilder import ZhegalkinPolynomialBuilder
        builder = ZhegalkinPolynomialBuilder()
        polynomial = builder.build(function)

        return '&' not in polynomial or len(function.variables) == 1
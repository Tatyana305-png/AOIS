from typing import List, Tuple
from ..Models.BooleanFunction import BooleanFunction


class ZhegalkinPolynomialBuilder:
    """Построитель полинома Жегалкина методом треугольника (как в оригинальном коде)"""

    def build(self, function: BooleanFunction) -> str:
        """Построение полинома Жегалкина"""
        vector = function.truth_table.get_result_column()

        coefficients = self._compute_coefficients(vector, len(function.variables))

        monomials = []
        for mask, coeff in enumerate(coefficients):
            if coeff == 1:
                monomial = self._mask_to_monomial(mask, function.variables)
                if monomial:
                    monomials.append(monomial)

        if not monomials:
            return '0'

        def sort_key(monom):
            if monom == '1':
                return (0, monom)
            elif len(monom) == 1 and monom in 'abcde':
                return (1, monom)
            else:
                return (2, monom)

        monomials.sort(key=sort_key)
        return ' ⊕ '.join(monomials)

    def _compute_coefficients(self, vector: List[int], dimension: int) -> List[int]:
        """
        Вычисление коэффициентов полинома Жегалкина методом треугольника.
        Алгоритм из оригинального кода.
        """
        coefficients = vector.copy()

        for bit in range(dimension):
            bit_mask = 1 << bit
            for mask in range(1 << dimension):
                if mask & bit_mask:
                    coefficients[mask] ^= coefficients[mask ^ bit_mask]

        return coefficients

    def _mask_to_monomial(self, mask: int, variables: List[str]) -> str:
        """
        Преобразование маски в моном.
        mask=0 -> "1"
        mask=1 (001) -> "a" (если a - младший бит)
        mask=2 (010) -> "b"
        mask=4 (100) -> "c"
        mask=3 (011) -> "a&b"
        и т.д.
        """
        if mask == 0:
            return "1"

        parts = []
        n = len(variables)

        for i, var in enumerate(variables):

            bit = 1 << (n - 1 - i)
            if mask & bit:
                parts.append(var)

        if not parts:
            return "1"
        if len(parts) == 1:
            return parts[0]
        return '&'.join(parts)

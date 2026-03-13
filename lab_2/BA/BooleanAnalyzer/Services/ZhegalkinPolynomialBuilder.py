from typing import List
from ..Models.BooleanFunction import BooleanFunction


class ZhegalkinPolynomialBuilder:
    """Построитель полинома Жегалкина"""

    def build(self, function: BooleanFunction) -> str:
        """Построение полинома методом треугольника"""
        if len(function.variables) == 0:
            if function.expression == '0':
                return '0'
            else:
                return '1'

        results = function.truth_table.get_result_column()
        n = len(function.variables)

        coeffs = results.copy()
        step = 1
        while step < len(coeffs):
            for i in range(len(coeffs) - step):
                coeffs[i] = coeffs[i] ^ coeffs[i + step]
            step *= 2

        terms = self._coeffs_to_terms(coeffs, function.variables)

        if not terms:
            return '0'

        def sort_key(term):
            if term == '1':
                return (0, term)
            elif len(term) == 1 and term in 'abcde':
                return (1, term)
            else:
                return (2, term)

        terms.sort(key=sort_key)
        return ' ⊕ '.join(terms)

    def _coeffs_to_terms(self, coeffs: List[int], variables: List[str]) -> List[str]:
        """Преобразование коэффициентов в термы"""
        terms = []
        n = len(variables)

        for i, coeff in enumerate(coeffs):
            if coeff == 1:
                if i == 0:
                    terms.append('1')
                else:
                    bits = format(i, f'0{n}b')[::-1]
                    term_vars = [var for var, bit in zip(variables, bits) if bit == '1']
                    if len(term_vars) == 1:
                        terms.append(term_vars[0])
                    elif len(term_vars) > 1:
                        terms.append('&'.join(term_vars))
                    else:
                        terms.append('1')

        return terms
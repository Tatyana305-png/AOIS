from typing import List, Tuple, Set, Dict
from .BaseMinimizer import BaseMinimizer
from ...Models.BooleanFunction import BooleanFunction
from ..SDNFSKNFBuilder import StandardFormBuilder

class CalculationMinimizer(BaseMinimizer):
    """Минимизация расчетным методом (метод Квайна)"""

    def minimize(self, function: BooleanFunction) -> Tuple[str, List[str]]:
        """Минимизация функции"""
        builder = StandardFormBuilder(self.term_parser)
        sdnf, _ = builder.build(function)

        if sdnf == '0':
            return '0', ["Функция тождественно равна 0"]

        terms = self.term_parser.parse_dnf(sdnf)
        stages = [f"Исходная СДНФ: {' ∨ '.join(terms)}"]

        current_terms = terms.copy()
        all_implicants = []
        iteration = 1

        while True:
            new_terms, used = self._glue_step(current_terms, function.variables)

            for term in current_terms:
                if term not in used:
                    new_terms.add(term)

            if not new_terms or new_terms == set(current_terms):
                all_implicants = list(new_terms)
                break

            stages.append(f"Этап склеивания {iteration}: {' ∨ '.join(new_terms)}")
            current_terms = list(new_terms)
            iteration += 1

        essential = self._find_essential_implicants(all_implicants, function)

        if set(essential) != set(all_implicants):
            stages.append(f"После удаления лишних импликант: {' ∨ '.join(essential)}")

        simplified = self._simplify_result(essential)

        minimized = ' ∨ '.join(simplified) if simplified else '0'
        return minimized, stages

    def _glue_step(self, terms: List[str], variables: List[str]) -> Tuple[Set[str], Set[str]]:
        """Один шаг склеивания"""
        new_terms = set()
        used = set()

        for i, term1 in enumerate(terms):
            literals1 = self._parse_term_to_dict(term1)
            for j, term2 in enumerate(terms[i + 1:], i + 1):
                literals2 = self._parse_term_to_dict(term2)

                diff = self._find_difference(literals1, literals2)
                if len(diff) == 1:
                    common = {}
                    for var in set(literals1.keys()) & set(literals2.keys()):
                        if literals1[var] == literals2[var]:
                            common[var] = literals1[var]

                    if common:
                        glued = self._dict_to_term(common)
                        new_terms.add(glued)
                        used.add(term1)
                        used.add(term2)

        return new_terms, used

    def _parse_term_to_dict(self, term: str) -> Dict[str, int]:
        """Преобразование терма в словарь {переменная: значение}"""
        literals = self.term_parser.parse_term(term)
        result = {}
        for lit in literals:
            if lit.startswith('!'):
                result[lit[1:]] = 0
            else:
                result[lit] = 1
        return result

    def _dict_to_term(self, d: Dict[str, int]) -> str:
        """Преобразование словаря обратно в терм"""
        literals = []
        for var, val in sorted(d.items()):
            if val == 1:
                literals.append(var)
            else:
                literals.append(f'!{var}')
        return self.term_parser.join_literals(literals, '&')

    def _find_difference(self, dict1: Dict[str, int], dict2: Dict[str, int]) -> List[str]:
        """Поиск переменных, по которым отличаются два терма"""
        diff = []
        all_vars = set(dict1.keys()) | set(dict2.keys())
        for var in all_vars:
            val1 = dict1.get(var)
            val2 = dict2.get(var)
            if val1 != val2:
                diff.append(var)
        return diff

    def _find_essential_implicants(self, implicants: List[str],
                                   function: BooleanFunction) -> List[str]:
        """Поиск существенных импликант"""
        ones_sets = function.truth_table.get_ones_sets()

        if not ones_sets:
            return []

        coverage = {}
        for imp in implicants:
            covered = []
            for bits in ones_sets:
                if self._term_covers(imp, bits, function.variables):
                    covered.append(bits)
            if covered:
                coverage[imp] = covered

        essential = []
        covered_sets = set()

        for imp, covered in coverage.items():
            for bits in covered:
                count = 0
                for other_imp, other_covered in coverage.items():
                    if bits in other_covered:
                        count += 1
                if count == 1:
                    if imp not in essential:
                        essential.append(imp)
                        covered_sets.update(covered)
                    break

        remaining = [bits for bits in ones_sets if bits not in covered_sets]

        while remaining:
            best_imp = None
            best_count = 0
            best_covered = []

            for imp, covered in coverage.items():
                if imp in essential:
                    continue
                count = sum(1 for bits in remaining if bits in covered)
                if count > best_count:
                    best_count = count
                    best_imp = imp
                    best_covered = covered

            if best_imp:
                essential.append(best_imp)
                covered_sets.update(best_covered)
                remaining = [bits for bits in ones_sets if bits not in covered_sets]
            else:
                break

        return essential

    def _simplify_result(self, terms: List[str]) -> List[str]:
        """Упрощение результата (убираем тавтологии)"""
        if not terms:
            return []

        has_var = set()
        has_not_var = set()

        for term in terms:
            if len(term) == 1 and term in 'abcde':
                has_var.add(term)
            elif len(term) == 2 and term[0] == '!' and term[1] in 'abcde':
                has_not_var.add(term[1])

        for var in has_var & has_not_var:
            return [f'!{var} ∨ {var}']

        return terms

    def _term_covers(self, term: str, bits: Tuple[int, ...], variables: List[str]) -> bool:
        """Проверка, покрывает ли терм набор"""
        literals = self.term_parser.parse_term(term)
        var_dict = dict(zip(variables, bits))

        for lit in literals:
            if lit.startswith('!'):
                var = lit[1:]
                if var not in var_dict or var_dict[var] != 0:
                    return False
            else:
                if lit not in var_dict or var_dict[lit] != 1:
                    return False
        return True
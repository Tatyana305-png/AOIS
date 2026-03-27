from typing import List, Tuple, Set, Dict
from .BaseMinimizer import BaseMinimizer
from ...Models.BooleanFunction import BooleanFunction


class CalculationMinimizer(BaseMinimizer):
    """Минимизация расчетным методом (метод Квайна)"""

    def minimize(self, function: BooleanFunction) -> Tuple[str, List[str]]:
        """Минимизация функции - показывает оба метода"""
        from ..SDNFSKNFBuilder import StandardFormBuilder
        builder = StandardFormBuilder(self.term_parser)
        sdnf, sknf = builder.build(function)

        stages = []

        stages.append("=" * 50)
        stages.append("МИНИМИЗАЦИЯ ПО СДНФ (по единицам)")
        stages.append("=" * 50)
        result_dnf, stages_dnf = self._minimize_by_dnf(sdnf, function)
        stages.extend(stages_dnf)
        stages.append(f"Результат минимизации по СДНФ: {result_dnf}")

        stages.append("\n" + "=" * 50)
        stages.append("МИНИМИЗАЦИЯ ПО СКНФ (по нулям)")
        stages.append("=" * 50)
        result_cnf, stages_cnf = self._minimize_by_cnf(sknf, function)
        stages.extend(stages_cnf)
        stages.append(f"Результат минимизации по СКНФ: {result_cnf}")

        if len(result_dnf.replace(' ', '')) <= len(result_cnf.replace(' ', '')):
            stages.append("\n" + "=" * 50)
            stages.append(f"Лучший результат (по СДНФ): {result_dnf}")
            return result_dnf, stages
        else:
            stages.append("\n" + "=" * 50)
            stages.append(f"Лучший результат (по СКНФ): {result_cnf}")
            return result_cnf, stages

    def _minimize_by_dnf(self, dnf: str, function: BooleanFunction) -> Tuple[str, List[str]]:
        """Минимизация по СДНФ"""
        stages = []

        if dnf == '0':
            return '0', stages
        if dnf == '1':
            return '1', stages

        terms = self.term_parser.parse_dnf(dnf)
        stages.append(f"Исходная СДНФ: {' ∨ '.join(terms)}")

        current_terms = terms.copy()
        all_implicants = []
        iteration = 1

        while True:
            new_terms, used = self._glue_terms_dnf(current_terms, function.variables)

            for term in current_terms:
                if term not in used:
                    new_terms.add(term)

            if not new_terms or new_terms == set(current_terms):
                all_implicants = list(new_terms)
                break

            stages.append(f"Этап склеивания {iteration}: {' ∨ '.join(new_terms)}")
            current_terms = list(new_terms)
            iteration += 1

        stages.append(f"Все простые импликанты: {' ∨ '.join(all_implicants)}")

        essential = self._find_essential_implicants_dnf(all_implicants, function)

        if essential:
            stages.append(f"Существенные импликанты: {' ∨ '.join(essential)}")
        else:
            stages.append("Существенных импликант не найдено")

        result = ' ∨ '.join(essential) if essential else '0'
        return result, stages

    def _minimize_by_cnf(self, cnf: str, function: BooleanFunction) -> Tuple[str, List[str]]:
        """Минимизация по СКНФ"""
        stages = []

        if cnf == '1':
            return '1', stages
        if cnf == '0':
            return '0', stages

        terms = self.term_parser.parse_cnf(cnf)
        stages.append(f"Исходная СКНФ: {' ∧ '.join(terms)}")

        if len(terms) == 1:
            stages.append("СКНФ уже минимальна (состоит из одного терма)")
            return terms[0], stages

        current_terms = terms.copy()
        all_implicants = []
        iteration = 1

        while True:
            new_terms, used = self._glue_terms_cnf(current_terms, function.variables)

            for term in current_terms:
                if term not in used:
                    new_terms.add(term)

            if not new_terms or new_terms == set(current_terms):
                all_implicants = list(new_terms)
                break

            stages.append(f"Этап склеивания {iteration}: {' ∧ '.join(new_terms)}")
            current_terms = list(new_terms)
            iteration += 1

        stages.append(f"Все простые импликанты: {' ∧ '.join(all_implicants)}")

        essential = self._find_essential_implicants_cnf(all_implicants, function)

        if essential:
            stages.append(f"Существенные импликанты: {' ∧ '.join(essential)}")
        else:
            stages.append("Существенных импликант не найдено")

        result = ' ∧ '.join(essential) if essential else '1'
        return result, stages

    def _glue_terms_dnf(self, terms: List[str], variables: List[str]) -> Tuple[Set[str], Set[str]]:
        """Склеивание термов в ДНФ"""
        new_terms = set()
        used = set()

        for i, term1 in enumerate(terms):
            literals1 = set(self.term_parser.parse_term(term1))
            for j, term2 in enumerate(terms[i + 1:], i + 1):
                literals2 = set(self.term_parser.parse_term(term2))

                diff = literals1.symmetric_difference(literals2)

                if len(diff) == 2:
                    diff_list = list(diff)
                    lit1, lit2 = diff_list[0], diff_list[1]
                    if (lit1[0] == '!' and lit2 == lit1[1:]) or (lit2[0] == '!' and lit1 == lit2[1:]):
                        common = literals1.intersection(literals2)
                        if common:
                            glued = self.term_parser.join_literals(sorted(common), '&')
                            new_terms.add(glued)
                            used.add(term1)
                            used.add(term2)

        return new_terms, used

    def _glue_terms_cnf(self, terms: List[str], variables: List[str]) -> Tuple[Set[str], Set[str]]:
        """Склеивание термов в КНФ"""
        new_terms = set()
        used = set()

        for i, term1 in enumerate(terms):
            literals1 = set(self.term_parser.parse_term(term1))
            for j, term2 in enumerate(terms[i + 1:], i + 1):
                literals2 = set(self.term_parser.parse_term(term2))

                diff = literals1.symmetric_difference(literals2)

                if len(diff) == 2:
                    diff_list = list(diff)
                    lit1, lit2 = diff_list[0], diff_list[1]
                    if (lit1[0] == '!' and lit2 == lit1[1:]) or (lit2[0] == '!' and lit1 == lit2[1:]):
                        common = literals1.intersection(literals2)
                        if common:
                            glued = self.term_parser.join_literals(sorted(common), '|')
                            new_terms.add(glued)
                            used.add(term1)
                            used.add(term2)

        return new_terms, used

    def _find_essential_implicants_dnf(self, implicants: List[str],
                                       function: BooleanFunction) -> List[str]:
        """Поиск существенных импликант для ДНФ"""
        ones_sets = function.truth_table.get_ones_sets()

        if not ones_sets:
            return []

        coverage = {}
        for imp in implicants:
            covered = []
            for bits in ones_sets:
                if self._term_covers_dnf(imp, bits, function.variables):
                    covered.append(bits)
            if covered:
                coverage[imp] = covered

        essential = []
        covered_sets = set()

        for imp, covered in coverage.items():
            for bits in covered:
                count = sum(1 for other_covered in coverage.values() if bits in other_covered)
                if count == 1:
                    if imp not in essential:
                        essential.append(imp)
                        covered_sets.update(covered)

        remaining = [bits for bits in ones_sets if bits not in covered_sets]

        while remaining:
            best_imp = None
            best_count = 0

            for imp, covered in coverage.items():
                if imp in essential:
                    continue
                count = sum(1 for bits in remaining if bits in covered)
                if count > best_count:
                    best_count = count
                    best_imp = imp

            if best_imp:
                essential.append(best_imp)
                covered_sets.update(coverage[best_imp])
                remaining = [bits for bits in ones_sets if bits not in covered_sets]
            else:
                break

        return essential

    def _find_essential_implicants_cnf(self, implicants: List[str],
                                       function: BooleanFunction) -> List[str]:
        """Поиск существенных импликант для КНФ"""
        zeros_sets = function.truth_table.get_zeros_sets()

        if not zeros_sets:
            return []

        coverage = {}
        for imp in implicants:
            covered = []
            for bits in zeros_sets:
                if self._term_covers_cnf(imp, bits, function.variables):
                    covered.append(bits)
            if covered:
                coverage[imp] = covered

        essential = []
        covered_sets = set()

        for imp, covered in coverage.items():
            for bits in covered:
                count = sum(1 for other_covered in coverage.values() if bits in other_covered)
                if count == 1:
                    if imp not in essential:
                        essential.append(imp)
                        covered_sets.update(covered)

        remaining = [bits for bits in zeros_sets if bits not in covered_sets]

        while remaining:
            best_imp = None
            best_count = 0

            for imp, covered in coverage.items():
                if imp in essential:
                    continue
                count = sum(1 for bits in remaining if bits in covered)
                if count > best_count:
                    best_count = count
                    best_imp = imp

            if best_imp:
                essential.append(best_imp)
                covered_sets.update(coverage[best_imp])
                remaining = [bits for bits in zeros_sets if bits not in covered_sets]
            else:
                break

        return essential

    def _term_covers_dnf(self, term: str, bits: Tuple[int, ...], variables: List[str]) -> bool:
        """Проверка, покрывает ли терм ДНФ набор"""
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

    def _term_covers_cnf(self, term: str, bits: Tuple[int, ...], variables: List[str]) -> bool:
        """Проверка, покрывает ли терм КНФ набор (т.е. обращается в 1 на этом наборе)"""
        literals = self.term_parser.parse_term(term)
        var_dict = dict(zip(variables, bits))

        for lit in literals:
            if lit.startswith('!'):
                var = lit[1:]
                if var in var_dict and var_dict[var] == 0:
                    return True
            else:
                if lit in var_dict and var_dict[lit] == 1:
                    return True
        return False

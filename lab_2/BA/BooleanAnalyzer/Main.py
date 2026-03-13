import sys
from typing import Optional
from tabulate import tabulate

from BooleanAnalyzer.Models.BooleanFunction import BooleanFunction
from BooleanAnalyzer.Models.ExpressionParser import BooleanExpressionParser
from BooleanAnalyzer.Services.SDNFSKNFBuilder import StandardFormBuilder
from BooleanAnalyzer.Services.NumericFormConverter import NumericFormConverter
from BooleanAnalyzer.Services.PostClassChecker import PostClassChecker
from BooleanAnalyzer.Services.ZhegalkinPolynomialBuilder import ZhegalkinPolynomialBuilder
from BooleanAnalyzer.Services.FictitiousVariableFinder import FictitiousVariableFinder
from BooleanAnalyzer.Services.BooleanDerivativeCalculator import BooleanDerivativeCalculator
from BooleanAnalyzer.Services.Minimization.CalculationMinimizer import CalculationMinimizer
from BooleanAnalyzer.Services.Minimization.TableCalculationMinimizer import TableCalculationMinimizer
from BooleanAnalyzer.Services.Minimization.KarnaughMinimizer import KarnaughMinimizer
from BooleanAnalyzer.Utils.TermParser import TermParser
from BooleanAnalyzer.Utils.Validators import ExpressionValidator


class BooleanFunctionAnalyzer:
    """Анализатор булевых функций - основной класс приложения"""

    def __init__(self):
        self.parser = BooleanExpressionParser()
        self.term_parser = TermParser()
        self.validator = ExpressionValidator()

        self.sdnf_sknf_builder = StandardFormBuilder(self.term_parser)
        self.numeric_converter = NumericFormConverter()
        self.post_checker = PostClassChecker()
        self.zhegalkin_builder = ZhegalkinPolynomialBuilder()
        self.fictitious_finder = FictitiousVariableFinder()
        self.derivative_calculator = BooleanDerivativeCalculator()
        self.calc_minimizer = CalculationMinimizer()
        self.table_calc_minimizer = TableCalculationMinimizer()
        self.karnaugh_minimizer = KarnaughMinimizer()

        self.current_function: Optional[BooleanFunction] = None

    def analyze(self, expression: str) -> None:
        """Анализ булевой функции"""
        try:
            if not self.validator.validate(expression):
                print(f"Ошибка: Некорректное выражение '{expression}'")
                return

            self.current_function = BooleanFunction(expression, self.parser)

            self._print_results()

        except Exception as e:
            print(f"Ошибка при анализе: {e}")

    def _print_results(self) -> None:
        """Вывод всех результатов анализа"""
        if not self.current_function:
            return

        f = self.current_function

        print("=" * 70)
        print(f"АНАЛИЗ БУЛЕВОЙ ФУНКЦИИ: {f.expression}")
        print("=" * 70)

        self._print_truth_table(f)
        self._print_sdnf_sknf(f)
        self._print_numeric_forms(f)
        self._print_post_classes(f)
        self._print_zhegalkin(f)
        self._print_fictitious_vars(f)
        self._print_derivatives(f)
        self._print_minimization_results(f)

        print("=" * 70)

    def _print_truth_table(self, f: BooleanFunction) -> None:
        """Вывод таблицы истинности"""
        print("\n ТАБЛИЦА ИСТИННОСТИ")
        print("-" * 50)

        header = list(f.variables) + ['F']
        data = []
        for bits, result in f.truth_table:
            row = list(bits) + [result]
            data.append(row)

        print(tabulate(data, headers=header, tablefmt='grid'))

    def _print_sdnf_sknf(self, f: BooleanFunction) -> None:
        """Вывод СДНФ и СКНФ"""
        sdnf, sknf = self.sdnf_sknf_builder.build(f)
        print(f"\n СДНФ: {sdnf}")
        print(f" СКНФ: {sknf}")

    def _print_numeric_forms(self, f: BooleanFunction) -> None:
        """Вывод числовых форм"""
        sdnf_num, sknf_num = self.numeric_converter.convert(f)
        index_form = self.numeric_converter.get_index_form(f)

        print(f"\n Числовая форма СДНФ: {sdnf_num}")
        print(f" Числовая форма СКНФ: {sknf_num}")
        print(f" Индексная форма: {index_form}")

    def _print_post_classes(self, f: BooleanFunction) -> None:
        """Вывод классов Поста"""
        classes = self.post_checker.check_all(f)

        print("\n КЛАССЫ ПОСТА")
        for class_name, belongs in classes.items():
            status = "Y" if belongs else "N"
            print(f"  {status} {class_name}")

    def _print_zhegalkin(self, f: BooleanFunction) -> None:
        """Вывод полинома Жегалкина"""
        poly = self.zhegalkin_builder.build(f)
        print(f"\n Полином Жегалкина: {poly}")

    def _print_fictitious_vars(self, f: BooleanFunction) -> None:
        """Вывод фиктивных переменных"""
        fictitious = self.fictitious_finder.find(f)

        print("\n ФИКТИВНЫЕ ПЕРЕМЕННЫЕ")
        if fictitious:
            print(f"  Найдены: {', '.join(fictitious)}")
        else:
            print("  Фиктивных переменных нет")

    def _print_derivatives(self, f: BooleanFunction) -> None:
        """Вывод булевых производных"""
        print("\n БУЛЕВЫ ПРОИЗВОДНЫЕ")

        for var in f.variables:
            deriv = self.derivative_calculator.calculate(f, [var])
            print(f"  ∂F/∂{var}: {deriv}")

        if len(f.variables) >= 2:
            mixed = self.derivative_calculator.calculate(f, f.variables[:2])
            print(f"  ∂²F/∂{f.variables[0]}∂{f.variables[1]}: {mixed}")

    def _print_minimization_results(self, f: BooleanFunction) -> None:
        """Вывод результатов минимизации"""
        print("\n МИНИМИЗАЦИЯ")

        # Расчетный метод
        minimized_calc, stages_calc = self.calc_minimizer.minimize(f)
        print("\n  Расчетный метод:")
        for stage in stages_calc[-3:]:
            print(f"    {stage}")
        print(f"  Результат: {minimized_calc}")

        minimized_tcalc, stages_tcalc, table = self.table_calc_minimizer.minimize(f)
        print("\n  Расчетно-табличный метод:")
        print("  Таблица покрытия:")
        for line in table.split('\n'):
            print(f"    {line}")
        print(f"  Результат: {minimized_tcalc}")

        minimized_karn, karn_map = self.karnaugh_minimizer.minimize(f)
        print("\n  Табличный метод (карта Карно):")
        for line in karn_map.split('\n'):
            print(f"    {line}")
        print(f"  Результат: {minimized_karn}")


def main():
    """Точка входа в программу"""
    analyzer = BooleanFunctionAnalyzer()

    print(" АНАЛИЗАТОР БУЛЕВЫХ ФУНКЦИЙ")
    print("=" * 50)
    print("Поддерживаемые операции:")
    print("  &  - конъюнкция (AND)")
    print("  |  - дизъюнкция (OR)")
    print("  !  - отрицание (NOT)")
    print("  -> - импликация (IMPLIES)")
    print("  ~  - эквивалентность (EQUIV)")
    print("Переменные: a, b, c, d, e (до 5)")
    print("=" * 50)

    if len(sys.argv) > 1:
        expression = ' '.join(sys.argv[1:])
        analyzer.analyze(expression)
    else:

        while True:
            print("\nВведите выражение (или 'exit' для выхода, 'test' для тестового примера):")
            expr = input(">>> ").strip()

            if expr.lower() == 'exit':
                print("До свидания!")
                break
            elif expr.lower() == 'test':
                expr = "!(!a->!b)|c"
                print(f"Тестовый пример: {expr}")

            analyzer.analyze(expr)


if __name__ == "__main__":
    main()
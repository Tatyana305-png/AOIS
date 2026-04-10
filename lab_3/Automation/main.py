from bcd_summarizer import BCDSummarizer
from constants import DELIMITER, LOG_LEVEL_INFO
from parallel_adder import ParallelAdder
from subtractor_counter import SubtractorCounter
from subtractor_synthesizer import SubtractorSynthesizer, LogicInBasisNAND_NOR


def print_test_result(
    label: str,
    value_a: str,
    value_b: str,
    carry_in: bool,
    adder: ParallelAdder,
) -> None:
    print(DELIMITER)
    print(f"{LOG_LEVEL_INFO}{label}")
    print(f"Input  A: {value_a}")
    print(f"Input  B: {value_b}")
    print(f"Carry In: {1 if carry_in else 0}")
    print(f"Result S: {adder.get_result_string()}")
    print(f"Carry Out: {1 if adder.get_final_carry() else 0}")


def test_subtractor_synthesizer() -> None:
    """Тест синтезированного вычитающего счетчика на T-триггерах"""
    print(DELIMITER)
    print(f"{LOG_LEVEL_INFO}Синтезированный вычитающий счетчик (T-триггеры, базис НЕ-И-ИЛИ)")

    synthesizer = SubtractorSynthesizer()

    # Вывод таблицы переходов
    synthesizer.print_transition_table()

    # Демонстрация работы счетчика
    print(f"\n{LOG_LEVEL_INFO}Работа счетчика (3 полных цикла):")
    print("Такт | Q2 Q1 Q0 | Десятичное")
    print("-" * 35)

    for cycle in range(3):
        for step in range(8):
            print(f"  {step:2d}  |  {synthesizer.get_binary()}  |     {synthesizer.get_current_value()}")
            synthesizer.tick()
        print("  --- переполнение ---")

    # Проверка установки начального значения
    print(f"\n{LOG_LEVEL_INFO}Проверка установки начального значения:")
    synthesizer.set_value(5)
    print(f"Установлено значение 5: {synthesizer.get_binary()} = {synthesizer.get_current_value()}")

    for _ in range(3):
        synthesizer.tick()
        print(f"  Такт -> {synthesizer.get_binary()} = {synthesizer.get_current_value()}")


def main() -> None:
    # ========== Тест 1: Параллельный сумматор ==========
    adder = ParallelAdder()
    value_a = "1000"
    value_b = "0110"

    carry_in_true = True
    adder.process_addition(value_a, value_b, carry_in_true)
    print_test_result("Test 1: Addition with Carry", value_a, value_b, carry_in_true, adder)

    carry_in_false = False
    adder.process_addition(value_a, value_b, carry_in_false)
    print_test_result(
        "Test 2: Addition without Carry",
        value_a,
        value_b,
        carry_in_false,
        adder,
    )

    # ========== Тест 2: BCD сумматор (вариант А, n=2) ==========
    print(DELIMITER)
    bcd_processor = BCDSummarizer()
    bcd_a = "1000"
    bcd_b = "0110"
    bcd_processor.execute(bcd_a, bcd_b)

    print(DELIMITER)
    print(f"{LOG_LEVEL_INFO}BCD Addition Test (Variant A, Offset n=2)")
    print(f"Input A: {bcd_a} (8)")
    print(f"Input B: {bcd_b} (6)")
    print("Process: 8 + 6 + 2(offset) = 16")
    print(f"BCD Result (Tens Units): {bcd_processor.get_full_result()}")
    print(DELIMITER)

    # ========== Тест 3: Программный вычитающий счетчик (для сравнения) ==========
    counter = SubtractorCounter(3)
    print(DELIMITER)
    print(f"{LOG_LEVEL_INFO}Программный вычитающий счетчик (для проверки логики):")
    for step in range(10):
        print(
            f"Step {step:2d}: Decimal {counter.get_current_value_decimal()} | "
            f"Binary {counter.get_current_value_binary()}"
        )
        counter.tick()

    # ========== Тест 4: Синтезированный счетчик на T-триггерах ==========
    test_subtractor_synthesizer()

    # ========== Тест 5: Демонстрация базиса НЕ-И-ИЛИ ==========
    LogicInBasisNAND_NOR.demonstrate()

    print(DELIMITER)


if __name__ == "__main__":
    main()

"""
T-триггер (T flip-flop) для синтеза цифровых автоматов
Таблица переходов:
T | Q(t) | Q(t+1)
0 |  0   |   0
0 |  1   |   1
1 |  0   |   1
1 |  1   |   0

Характеристическое уравнение: Q(t+1) = T ⊕ Q(t)
"""


class TFlipFlop:
    def __init__(self, initial_state: bool = False) -> None:
        """Инициализация T-триггера"""
        self.current_state = initial_state
        self.next_state = initial_state

    def tick(self, t_input: bool) -> None:
        """
        Тактовый импульс. Обновляет состояние в зависимости от входа T.
        Q(t+1) = T ⊕ Q(t)
        """
        self.next_state = t_input ^ self.current_state
        self.current_state = self.next_state

    def get_state(self) -> bool:
        """Получить текущее состояние"""
        return self.current_state

    def get_state_int(self) -> int:
        """Получить текущее состояние как int (0 или 1)"""
        return 1 if self.current_state else 0

    def set_state(self, state: bool) -> None:
        """Принудительно установить состояние"""
        self.current_state = state
        self.next_state = state

    def reset(self) -> None:
        """Сбросить триггер в 0"""
        self.current_state = False
        self.next_state = False


class TFlipFlopWithLogic:
    """
    T-триггер с поддержкой синтеза логики.
    Используется для построения счетчиков в базисе НЕ-И-ИЛИ.
    """

    def __init__(self, name: str = "", initial_state: bool = False) -> None:
        self.name = name
        self.current_state = initial_state
        self.next_state = initial_state
        self.t_input = False

    @staticmethod
    def characteristic_equation(t: bool, q: bool) -> bool:
        """Характеристическое уравнение T-триггера: Q_next = T ⊕ Q"""
        return t ^ q

    def compute_next_state(self, t_input: bool) -> bool:
        """Вычислить следующее состояние без обновления"""
        return self.characteristic_equation(t_input, self.current_state)

    def update(self, t_input: bool) -> None:
        """Обновить состояние"""
        self.t_input = t_input
        self.next_state = self.compute_next_state(t_input)
        self.current_state = self.next_state

    def get_t_input(self) -> bool:
        return self.t_input

    def __repr__(self) -> str:
        return f"TFlipFlop({self.name}: Q={1 if self.current_state else 0})"
class Record:
    """Класс для хранения записи в хеш-таблице"""

    def __init__(self, key_id, data, key_word=None):
        """
        Инициализация записи

        Args:
            key_id: идентификатор ключевого слова
            data: данные (определение, описание)
            key_word: ключевое слово (полное)
        """
        self.key_id = key_id
        self.key_word = key_word
        self.data = data
        self.c_flag = 0
        self.u_flag = 1
        self.t_flag = 1
        self.l_flag = 0
        self.d_flag = 0
        self.po = -1

    def mark_deleted(self):
        """Пометить запись как удаленную"""
        self.d_flag = 1
        self.u_flag = 0

    def is_deleted(self):
        """Проверить, помечена ли запись как удаленная"""
        return self.d_flag == 1

    def is_occupied(self):
        """Проверить, занята ли запись"""
        return self.u_flag == 1 and not self.is_deleted()

    def to_dict(self):
        """Преобразовать запись в словарь для вывода"""
        return {
            'ID': self.key_word or self.key_id,
            'C': self.c_flag,
            'U': self.u_flag,
            'T': self.t_flag,
            'L': self.l_flag,
            'D': self.d_flag,
            'Po': self.po if self.po != -1 else '',
            'Pi': self.data
        }

    def __str__(self):
        return f"Record({self.key_id}, data={self.data[:20] if self.data else ''}..., flags: C={self.c_flag}, U={self.u_flag}, T={self.t_flag}, L={self.l_flag}, D={self.d_flag}, Po={self.po})"
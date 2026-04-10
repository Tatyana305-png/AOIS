class Node:
    """Узел для связного списка (разрешение коллизий)"""

    def __init__(self, record, index):
        """
        Инициализация узла

        Args:
            record: запись Record
            index: индекс в хеш-таблице
        """
        self.record = record
        self.index = index
        self.next = None

    def __str__(self):
        return f"Node(index={self.index}, record={self.record.key_id})"
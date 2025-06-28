import os
import re
import random
from defaultClasses import Task


class Parser:
    """
    Парсер задач из GUI и любого файла
    Ожидает строки: time deadline.
    Примеры корректных строк:
        3,5
        4 12
        2,  8
        7 ,,9
        12 ,  21
        или
        3 5\n4,12\n2 ,, 8\n
    """

    def __init__(self, source: str):
        self.source = source
        self._is_file = os.path.exists(source) and os.path.isfile(source)

    def get_tasks(self) -> list[Task]:
        lines = []
        if self._is_file:
            with open(self.source, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        else:
            lines = self.source.splitlines()

        tasks: list[Task] = []
        for lineno, raw in enumerate(lines, start=1):
            line = raw.strip()
            if not line:
                continue  # пустые строки игнорируем

            # разбиваем по запятой/ым и/или любому количеству пробелов
            parts = re.split(r'[,\s]+', line)
            if len(parts) != 2:
                raise ValueError(f"Строка {lineno}: ожидаются два числа, получено: '{line}'")

            try:
                time = int(parts[0])
                deadline = int(parts[1])
            except ValueError:
                raise ValueError(f"Строка {lineno}: неверный формат целых чисел: '{parts[0]}' или '{parts[1]}'")

            # Task сам проверит неотрицательность
            tasks.append(Task(time=time, deadline=deadline))

        if not tasks:
            raise ValueError("Нет ни одной валидной строки с задачами.")
        return tasks


class RandomParser:
    def __init__(self,
                 n: int,  # число задач
                 time_range: tuple[int, int] = (1, 10),  # (min_time, max_time)
                 deadline_range: tuple[int, int] = (1, 20)):  # (min_deadline, max_deadline)
        if n < 1:
            raise ValueError("Количество задач должно быть ≥ 1")
        self.n = n
        self.min_time, self.max_time = time_range
        self.min_dead, self.max_dead = deadline_range
        if not (0 <= self.min_time <= self.max_time and
                0 <= self.min_dead <= self.max_dead):
            raise ValueError("Неправильный диапазон времени/дедлайна")

    def get_tasks(self) -> list[Task]:
        tasks: list[Task] = []
        for _ in range(self.n):
            t = random.randint(self.min_time, self.max_time)
            d = random.randint(self.min_dead, self.max_dead)
            # чтобы дедлайн не был меньше времени
            if d < t:
                d = t + random.randint(0, self.max_time)
            tasks.append(Task(time=t, deadline=d))
        return tasks

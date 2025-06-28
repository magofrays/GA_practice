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

    @staticmethod
    def get_tasks(source: str) -> list[Task]:
        if os.path.exists(source) and os.path.isfile(source):
            lines = open(source, 'r', encoding='utf-8').read().splitlines()
        else:
            lines = source.splitlines()

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
    @staticmethod
    def get_tasks(n: int,
                  time_range: tuple[int, int] = (1, 10),
                  deadline_range: tuple[int, int] = (1, 20)
                  ) -> list[Task]:
        if n < 1:
            raise ValueError("Количество задач должно быть ≥ 1")
        min_t, max_t = time_range
        min_d, max_d = deadline_range
        if not (0 <= min_t <= max_t and 0 <= min_d <= max_d):
            raise ValueError("Неправильный диапазон времени/дедлайна")
        tasks: list[Task] = []
        for _ in range(n):
            time = random.randint(min_t, max_t)
            deadline = random.randint(min_d, max_d)
            # чтобы дедлайн не был меньше времени
            if deadline < time:
                deadline = time + random.randint(0, max_t)
            tasks.append(Task(time=time, deadline=deadline))
        return tasks

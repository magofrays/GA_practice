import csv
import random
from defaultClasses import Task


class Parser:
    """
    Парсер задач из CSV-файла.
    Ожидает файл со строками: time, deadline
    Пример входных строк:
        3,5
        2,8
        7,4
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_tasks(self) -> list[Task]:
        tasks: list[Task] = []
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # пропускаем пустые или строку-заголовок (если там буквы)
                if not row or any(cell.isalpha() for cell in row):
                    continue
                time, deadline = map(int, row[:2])
                tasks.append(Task(time=time, deadline=deadline))
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

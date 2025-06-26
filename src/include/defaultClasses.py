from dataclasses import dataclass
import csv  # для дальнейшего чтения исходных данных 
from typing import List

class Task:
    _next_id = 0 # статическая переменная
    def __init__(self, time : int, deadline : int):
        self.time = time
        self.deadline = deadline
        self.id = Task._next_id # у каждого таска свой id
        Task._next_id += 1 
        self._validate()

    def _validate(self):
        if self.time < 0 or self.deadline < 0:
            raise ValueError("Число времени и дедлайна должно быть неотрицательным.")

@dataclass
class ParamGeneticAlgorithm:  # параметры ГА
    crossover: float = 0.5          # Вероятность скрещивания (0-1)
    mutation: float = 0.5           # Вероятность мутации (0-1)
    num_individuals: int = 150      # Размер популяции (≥2)
    num_generations: int = 100      # Количество поколений (≥1)

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Проверка корректности значений."""
        if self.num_individuals < 2 or self.num_generations < 1:
            raise ValueError("Популяция должна быть ≥2, поколения ≥1.")
        if not (0 <= self.crossover <= 1 and 0 <= self.mutation <= 1):
            raise ValueError("Вероятности должны быть в диапазоне [0, 1].")


class ScheduleInfo:  # класс, представляющий конкретную особь (последовательность задач)
    def __init__(self, order: List[int], tasks: List[Task]):
        self.order = order.copy()  # копируем последовательность индексов задач
        self.tasks = tasks  # ссылка на список задач
        self.tardiness = self._calculate_tardiness()  # общая задержка

    def _calculate_tardiness(self) -> int:  # целевая функция - общая задержка
        # (можно поменять и добавить возможность вычисления каждой отдельной задержки)
        current_time = 0
        total_tardiness = 0
        for idx in self.order:
            task = self.tasks[idx]
            current_time += task.time
            total_tardiness += max(0, current_time - task.deadline)
        return total_tardiness

    def copy(self):
        return ScheduleInfo(self.order, self.tasks)

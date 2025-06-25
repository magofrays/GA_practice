from dataclasses import dataclass

import csv  # для дальнейшего чтения исходных данных
import random  # для дальнейшего чтения исходных данных
from typing import List

@dataclass
class Task:
    time: int  # время выполнения задачи
    deadline: int  # дедлайн задачи

    def __post_init__(self):
        if self.time < 0 or self.deadline < 0:
            raise ValueError("Число времени и дедлайна должно быть неотрицательным.")


@dataclass
class ParamProbability:  # параметры вероятности
    crossover: float  # вероятность скрещивания
    mutation: float  # вероятность мутации

    def __post_init__(self):
        if not (0 <= self.crossover <= 1 and 0 <= self.mutation <= 1):
            raise ValueError("Параметры вероятностей должны быть в [0, 1].")


@dataclass
class ParamGeneticAlgorithm:  # параметры ГА
    probability: ParamProbability
    num_individuals: int  # размер популяции
    num_generations: int  # количество поколений

    def __post_init__(self):
        if self.num_individuals < 2 or self.num_generations < 1:
            raise ValueError("Неверные параметры популяции или поколений.")


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

from dataclasses import dataclass, field

import csv  # для дальнейшего чтения исходных данных
import random  # для дальнейшего чтения исходных данных
from typing import List

@dataclass
class Task:
    time: int
    deadline: int
    id: int = field(init=False)
    _next_id: int = field(default=0, init=False, repr=False)

    def __post_init__(self):
        self.id = Task._next_id
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
    num_to_select : int = 50
    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Проверка корректности значений."""
        if self.num_individuals < 2 or self.num_generations < 1:
            raise ValueError("Популяция должна быть ≥2, поколения ≥1.")
        if not (0 <= self.crossover <= 1 and 0 <= self.mutation <= 1):
            raise ValueError("Вероятности должны быть в диапазоне [0, 1].")
        if self.num_to_select < 2:
            raise ValueError("Отбираться должно больше 1 особи!")


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

class State:
    SELECTION = 0
    CROSSBREEDING = 1
    MUTATION = 2    
    INIT = 4

@dataclass
class GenerationState:  # состояние одного поколения
    population: List[ScheduleInfo]     # список всех особей
    state: State # является ли скрещиванием
    best: ScheduleInfo = field(init=False)
    average_tardiness: float = field(init=False)

    
    id: int = field(init=False)
    _next_id: int = field(default=0, init=False, repr=False)
    def __post_init__(self):
        self.best = min(self.population, key=lambda s: s.tardiness)  # лучшая особь по минимальной задержке
        total = sum(s.tardiness for s in self.population)
        self.average_tardiness = total / len(self.population)  # средняя задержка по популяции
        self.id = GenerationState._next_id
        GenerationState._next_id += 1

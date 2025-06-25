from dataclasses import dataclass

import csv  # для дальнейшего чтения исходных данных
import random  # для дальнейшего чтения исходных данных


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


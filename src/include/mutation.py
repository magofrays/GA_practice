from defaultClasses import ScheduleInfo
from abc import ABC, abstractmethod
from typing import List
import random


class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self,
               offspring: List[ScheduleInfo],
               mutation_rate: float
               ) -> List[ScheduleInfo]:
        """
        Мутирование с вероятностью mutation_rate к каждой особи.
        """


class NoMutation(MutationStrategy):
    def mutate(self, offspring: List[ScheduleInfo], rate: float) -> List[ScheduleInfo]:
        return [ind.copy() for ind in offspring]


# обмен двух генов
class SwapMutation(MutationStrategy):
    def mutate(self, offspring: List[ScheduleInfo], rate: float) -> List[ScheduleInfo]:
        mutated = []
        for ind in offspring:
            chrom = ind.order.copy()
            if random.random() < rate:
                i, j = random.sample(range(len(chrom)), 2)
                chrom[i], chrom[j] = chrom[j], chrom[i]
            mutated.append(ScheduleInfo(chrom, ind.tasks))
        return mutated


# инверсия случайного участка
class InversionMutation(MutationStrategy):
    def mutate(self, offspring: List[ScheduleInfo], rate: float) -> List[ScheduleInfo]:
        mutated = []
        for ind in offspring:
            chrom = ind.order.copy()
            if random.random() < rate:
                i, j = sorted(random.sample(range(len(chrom)), 2))
                chrom[i:j + 1] = reversed(chrom[i:j + 1])
            mutated.append(ScheduleInfo(chrom, ind.tasks))
        return mutated

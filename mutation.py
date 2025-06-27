from defaultClasses import ScheduleInfo, GenerationState, State
from abc import ABC, abstractmethod
from typing import List
import random


class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self,
               offspring: List[ScheduleInfo],
               mutation_rate: float
               ) -> GenerationState:
        """
        Мутирование с вероятностью mutation_rate к каждой особи.
        """


class NoMutation(MutationStrategy):
    def mutate(self, offspring: List[ScheduleInfo], rate: float) -> GenerationState:
        new_pop = [ind.copy() for ind in offspring]
        return GenerationState(population=new_pop, state=State.MUTATION)

# обмен двух генов
class SwapMutation(MutationStrategy):
    def mutate(self, offspring: List[ScheduleInfo], rate: float) -> GenerationState:
        mutated: List[ScheduleInfo] = []
        for ind in offspring:
            chrom = ind.order.copy()
            if random.random() < rate:
                i, j = random.sample(range(len(chrom)), 2)
                chrom[i], chrom[j] = chrom[j], chrom[i]
            mutated.append(ScheduleInfo(chrom, ind.tasks))
        return GenerationState(population=mutated, state=State.MUTATION)


# инверсия случайного участка
class InversionMutation(MutationStrategy):
    def mutate(self, offspring: List[ScheduleInfo], rate: float) -> GenerationState:
        mutated: List[ScheduleInfo] = []
        for ind in offspring:
            chrom = ind.order.copy()
            if random.random() < rate:
                i, j = sorted(random.sample(range(len(chrom)), 2))
                chrom[i:j+1] = list(reversed(chrom[i:j+1]))
            mutated.append(ScheduleInfo(chrom, ind.tasks))
        return GenerationState(population=mutated, state=State.MUTATION)

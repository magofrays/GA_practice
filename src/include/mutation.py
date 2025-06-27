from defaultClasses import ScheduleInfo, GenerationState, State
from abc import ABC, abstractmethod
from typing import List
import random


class MutationStrategy(ABC):
    @abstractmethod
    def mutate(self,
               state: GenerationState,
               mutation_rate: float
               ) -> GenerationState:
        """
        Мутирование с вероятностью mutation_rate к каждой особи.
        """


class NoMutation(MutationStrategy):
    def mutate(self, state: GenerationState, mutation_rate: float) -> GenerationState:
        new_pop = [ind.copy() for ind in state.population]
        return GenerationState(population=new_pop, state=State.MUTATION)


# обмен двух генов
class SwapMutation(MutationStrategy):
    def mutate(self, state: GenerationState, mutation_rate: float) -> GenerationState:
        mutated: List[ScheduleInfo] = []
        for ind in state.population:
            chrom = ind.order.copy()
            if random.random() < mutation_rate:
                i, j = random.sample(range(len(chrom)), 2)
                chrom[i], chrom[j] = chrom[j], chrom[i]
            mutated.append(ScheduleInfo(chrom, ind.tasks))
        return GenerationState(population=mutated, state=State.MUTATION)


# инверсия случайного участка
class InversionMutation(MutationStrategy):
    def mutate(self, state: GenerationState, mutation_rate: float) -> GenerationState:
        mutated: List[ScheduleInfo] = []
        for ind in state.population:
            chrom = ind.order.copy()
            if random.random() < mutation_rate:
                i, j = sorted(random.sample(range(len(chrom)), 2))
                chrom[i:j + 1] = list(reversed(chrom[i:j + 1]))
            mutated.append(ScheduleInfo(chrom, ind.tasks))
        return GenerationState(population=mutated, state=State.MUTATION)

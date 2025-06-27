from defaultClasses import ScheduleInfo, GenerationState, State
from abc import ABC, abstractmethod
from typing import List
import random


class SelectionStrategy(ABC):
    @abstractmethod
    def select(self,
               state: GenerationState,
               num_to_select: int
               ) -> GenerationState:
        """
        Выбираем из популяции num_to_select особей для скрещивания.
        """


class TournamentSelection(SelectionStrategy):
    def select(self, state: GenerationState, k: int) -> GenerationState:
        pop = state.population
        selected: List[ScheduleInfo] = []
        for _ in range(k):
            a, b = random.sample(pop, 2)
            winner = a if a.tardiness <= b.tardiness else b
            selected.append(winner.copy())
        return GenerationState(population=selected, state=State.SELECTION)


class RankSelection(SelectionStrategy):
    def select(self, state: GenerationState, k: int) -> GenerationState:
        sorted_pop = sorted(state.population, key=lambda ind: ind.tardiness)
        N = len(sorted_pop)
        weights = [N - i for i in range(N)]
        chosen = random.choices(sorted_pop, weights=weights, k=k)
        selected = [ind.copy() for ind in chosen]
        return GenerationState(population=selected, state=State.SELECTION)


class StochasticUniversalSampling(SelectionStrategy):
    def select(self, state: GenerationState, k: int) -> GenerationState:
        pop = state.population
        epsilon = 1e-6
        fitnesses = [1.0 / (ind.tardiness + epsilon) for ind in pop]
        total = sum(fitnesses)
        probs = [f / total for f in fitnesses]

        # кумулятивное распределение
        cum = []
        cumsum = 0.0
        for p in probs:
            cumsum += p
            cum.append(cumsum)

        # стартовая точка и указатели
        start = random.uniform(0, 1.0 / k)
        pointers = [start + i * (1.0 / k) for i in range(k)]

        selected: List[ScheduleInfo] = []
        idx = 0
        for ptr in pointers:
            while cum[idx] < ptr:
                idx += 1
            selected.append(pop[idx].copy())

        return GenerationState(population=selected, state=State.SELECTION)

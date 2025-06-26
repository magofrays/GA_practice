from defaultClasses import ScheduleInfo, GenerationState, State
from abc import ABC, abstractmethod
from typing import List
import random


class SelectionStrategy(ABC):
    @abstractmethod
    def select(self,
               population: List[ScheduleInfo],
               num_to_select: int
               ) -> GenerationState:
        """
        Выбираем из популяции num_to_select особей для скрещивания.
        """


class TournamentSelection(SelectionStrategy):
    def select(self, population: List[ScheduleInfo], k: int) -> GenerationState:
        selected = []
        for _ in range(k):
            a, b = random.sample(population, 2)
            winner = a if a.tardiness <= b.tardiness else b
            selected.append(winner.copy())
        return GenerationState(selected, State.SELECTION)


class RankSelection(SelectionStrategy):
    def select(self, population: List[ScheduleInfo], k: int) -> GenerationState:
        sorted_pop = sorted(population, key=lambda s: s.tardiness)
        N = len(sorted_pop)
        weights = [N - i for i in range(N)]
        chosen = random.choices(sorted_pop, weights=weights, k=k)
        selected = [ind.copy() for ind in chosen]
        return GenerationState(selected, State.SELECTION)


class StochasticUniversalSampling(SelectionStrategy):
    def select(self, population: List[ScheduleInfo], k: int) -> GenerationState:
        epsilon = 1e-6
        fitnesses = [1 / (ind.tardiness + epsilon) for ind in population]
        total_f = sum(fitnesses)
        probs = [f / total_f for f in fitnesses]
        cum = []
        csum = 0.0
        for p in probs:
            csum += p
            cum.append(csum)
        start = random.uniform(0, 1.0 / k)
        pointers = [start + i * (1.0 / k) for i in range(k)]
        selected = []
        idx = 0
        for ptr in pointers:
            while cum[idx] < ptr:
                idx += 1
            selected.append(population[idx].copy())
        return GenerationState(selected, State.SELECTION)

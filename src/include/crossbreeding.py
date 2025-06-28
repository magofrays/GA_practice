from defaultClasses import ScheduleInfo, GenerationState, State
from abc import ABC, abstractmethod
from typing import List
import random


class CrossbreedingStrategy(ABC):
    @abstractmethod
    def crossbreed(self,
                   state: GenerationState,
                   num_to_produce: int,
                   rate: float
                   ) -> GenerationState:
        """
        Берет selected отобранных особей и возвращает
        num_to_produce потомков.
        """


class OrderCrossbreeding(CrossbreedingStrategy):
    def crossbreed(self, state: GenerationState, num_to_produce: int, rate: float) -> GenerationState:
        parents = state.population.copy()
        random.shuffle(parents)
        n = len(parents[0].order)
        offspring: List[ScheduleInfo] = []

        for i in range(0, len(parents), 2):
            if len(offspring) >= num_to_produce:
                break
            p1, p2 = parents[i], parents[(i + 1) % len(parents)]
            if random.random() < rate:
                # генерируем двух потомков
                for a, b in [(p1.order, p2.order), (p2.order, p1.order)]:
                    child = [-1] * n
                    i1, i2 = sorted(random.sample(range(n), 2))
                    # копируем отрезок
                    child[i1:i2 + 1] = a[i1:i2 + 1]
                    pos = (i2 + 1) % n
                    # заполняем остаток генами из b
                    for gene in b[i2 + 1:] + b[:i2 + 1]:
                        if gene not in child:
                            child[pos] = gene
                            pos = (pos + 1) % n
                    offspring.append(ScheduleInfo(child, p1.tasks))
                    if len(offspring) >= num_to_produce:
                        break
            else:
                # копируем без изменений
                offspring.append(p1.copy())
                if len(offspring) < num_to_produce:
                    offspring.append(p2.copy())

        # досоздаем, если не хватило
        while len(offspring) < num_to_produce:
            offspring.append(random.choice(state.population).copy())

        return GenerationState(population=offspring[:num_to_produce],
                               state=State.CROSSBREEDING)

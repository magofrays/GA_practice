from defaultClasses import ScheduleInfo, GenerationState, State
from abc import ABC, abstractmethod
from typing import List
import random


class CrossbreedingStrategy(ABC):
    @abstractmethod
    def crossbreeding(self,
                      selected: List[ScheduleInfo],
                      num_to_produce: int,
                      rate: float
                      ) -> GenerationState:
        """
        Берет selected отобранных особей и возвращает
        num_to_produce потомков.
        """


# Одноточечное скрещивание
class SinglePointCrossbreeding(CrossbreedingStrategy):
    def crossbreeding(self,
                      selected: List[ScheduleInfo],
                      num_to_produce: int,
                      rate: float
                      ) -> GenerationState:
        n = len(selected[0].order)
        offspring: List[ScheduleInfo] = []
        parents = selected.copy()
        random.shuffle(parents)

        # генерируем потомков
        for i in range(0, len(parents), 2):
            if len(offspring) >= num_to_produce:
                break
            p1, p2 = parents[i], parents[(i + 1) % len(parents)]
            if random.random() < rate:
                cut = random.randrange(1, n)
                c1 = p1.order[:cut] + p2.order[cut:]
                c2 = p2.order[:cut] + p1.order[cut:]
            else:
                c1, c2 = p1.order.copy(), p2.order.copy()

            offspring.append(ScheduleInfo(c1, p1.tasks))
            if len(offspring) < num_to_produce:
                offspring.append(ScheduleInfo(c2, p1.tasks))

        # добираем, если не хватает
        while len(offspring) < num_to_produce:
            parent = random.choice(selected)
            offspring.append(parent.copy())

        return GenerationState(population=offspring[:num_to_produce],
                               state=State.CROSSBREEDING)


# Равномерное скрещивание
class UniformCrossbreeding(CrossbreedingStrategy):
    # С равной вероятностью берем ген из первого родителя,
    # иначе из второго.

    def crossbreeding(self,
                      selected: List[ScheduleInfo],
                      num_to_produce: int,
                      rate: float
                      ) -> GenerationState:
        # rate задает только вероятность применения операции к каждой паре
        offspring: List[ScheduleInfo] = []
        parents = selected.copy()
        random.shuffle(parents)

        for i in range(0, len(parents), 2):
            if len(offspring) >= num_to_produce:
                break
            p1, p2 = parents[i], parents[(i + 1) % len(parents)]
            if random.random() < rate:
                c1, c2 = [], []
                for g1, g2 in zip(p1.order, p2.order):
                    if random.random() < 0.5:
                        c1.append(g1)
                        c2.append(g2)
                    else:
                        c1.append(g2)
                        c2.append(g1)
            else:
                c1, c2 = p1.order.copy(), p2.order.copy()

            offspring.append(ScheduleInfo(c1, p1.tasks))
            if len(offspring) < num_to_produce:
                offspring.append(ScheduleInfo(c2, p1.tasks))

        # дополняем, если не хватило
        while len(offspring) < num_to_produce:
            arm = random.choice(selected)
            offspring.append(arm.copy())

        return GenerationState(population=offspring[:num_to_produce],
                               state=State.CROSSBREEDING)


# Имитация двоичного скрещивания
class SimulatedBinaryCrossbreeding(CrossbreedingStrategy):
    # offspring1[i] = 0.5*((1+β)*p1 + (1-β)*p2)
    # offspring2[i] = 0.5*((1-β)*p1 + (1+β)*p2)

    def __init__(self, eta: float):
        if eta <= 0:
            raise ValueError("eta must be > 0")
        self.eta = eta

    def crossbreeding(self,
                      selected: List[ScheduleInfo],
                      num_to_produce: int,
                      rate: float
                      ) -> GenerationState:
        offspring: List[ScheduleInfo] = []
        parents = selected.copy()
        random.shuffle(parents)

        for i in range(0, len(parents), 2):
            if len(offspring) >= num_to_produce:
                break
            p1, p2 = parents[i], parents[(i + 1) % len(parents)]
            if random.random() < rate:
                c1, c2 = [], []
                for x, y in zip(p1.order, p2.order):
                    u = random.random()
                    if u <= 0.5:
                        beta = (2 * u) ** (1.0 / (self.eta + 1))
                    else:
                        beta = (1.0 / (2 * (1 - u))) ** (1.0 / (self.eta + 1))
                    val1 = 0.5 * ((1 + beta) * x + (1 - beta) * y)
                    val2 = 0.5 * ((1 - beta) * x + (1 + beta) * y)
                    c1.append(val1)
                    c2.append(val2)
            else:
                c1, c2 = p1.order.copy(), p2.order.copy()

            offspring.append(ScheduleInfo(c1, p1.tasks))
            if len(offspring) < num_to_produce:
                offspring.append(ScheduleInfo(c2, p1.tasks))

        while len(offspring) < num_to_produce:
            arm = random.choice(selected)
            offspring.append(arm.copy())

        return GenerationState(population=offspring[:num_to_produce],
                               state=State.CROSSBREEDING)

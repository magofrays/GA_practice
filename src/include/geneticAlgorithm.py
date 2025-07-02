from defaultClasses import ParamGeneticAlgorithm, ScheduleInfo, GenerationState, State, Task
from crossbreeding import CrossbreedingStrategy, OrderCrossbreeding
from mutation import MutationStrategy, NoMutation, SwapMutation
from selection import SelectionStrategy, TournamentSelection
import random
from typing import List

class geneticAlgorithm:
    def __init__(self):
        self.params = ParamGeneticAlgorithm()
        self.iteration = 0  # id популяции
        self.selection: SelectionStrategy = TournamentSelection()  # по стандарту турнир
        self.crossbreeding: CrossbreedingStrategy = OrderCrossbreeding()
        self.mutation: MutationStrategy = SwapMutation()
        self.generationState: GenerationState = None
        self.history: list[GenerationState] = []
        self.tasks = []

    def set_tasks(self, tasks):
        self.tasks = tasks
    
    def change_params(self, crossover: float, mutation: float, num_individuals: int, num_generations: int, num_to_select : int):
        self.params.crossover = crossover
        self.params.mutation = mutation
        self.params.num_individuals = num_individuals
        self.params.num_generations = num_generations
        self.params.num_to_select = num_to_select
        self.params._validate()

    def create_individuals(self):
        if len(self.tasks) == 0:
            raise ValueError("Не заданы задачи, для которых алгоритм ищет решение!")
        population = []
        for _ in range(self.params.num_individuals):
            order = list(range(len(self.tasks)))
            random.shuffle(order)
            population.append(ScheduleInfo(order, self.tasks))
        self.generationState = GenerationState(population, State.INIT)
        self.history.append(self.generationState)

    def change_selection(self, new_selection):
        self.selection = new_selection

    def change_crossbreading(self, new_crossbreading):
        self.crossbreeding = new_crossbreading

    def change_mutation(self, new_mutation):
        self.mutation = new_mutation

    def do_selection(self):
        self.generationState = self.selection.select(self.generationState, self.params.num_to_select)

    def do_crossbreeding(self):
        self.generationState = self.crossbreeding.crossbreed(
            self.generationState,
            self.params.num_individuals,
            self.params.crossover
        )

    def do_mutation(self):
        self.generationState = self.mutation.mutate(
            self.generationState,
            self.params.mutation
        )
        self.iteration += 1

    def do_next(self):
        st = self.generationState.state

        if st == State.INIT:
            self.do_selection()

        elif st == State.SELECTION:
            self.do_crossbreeding()

        elif st == State.CROSSBREEDING:
            self.do_mutation()

        elif st == State.MUTATION:
            # отмечаем новое поколение и сразу стартуем отбор, если надо
            if self.iteration < self.params.num_generations:
                self.do_selection()
            else:
                raise ValueError("Невозможно идти вперед: алгоритм закончил свою работу!")
        self.history.append(self.generationState)

    def go_to_start(self):
        ScheduleInfo.reset_id()
        self.generationState = None
        if self.history:
            self.iteration = 0
            self.history = []

    def go_back(self):
        if len(self.history) == 1:
            raise ValueError("Невозможно вернуться назад: алгоритм только начал работу!")
        self.history.pop()
        prev = self.history[-1]
        if prev.state == State.MUTATION:
            self.iteration -= 1
        self.generationState = prev

    def finish(self):
        while self.generationState.state != State.MUTATION:
            self.do_next()

        while self.iteration < self.params.num_generations:
            self.do_next()

    def get_best(self) -> ScheduleInfo:
        if not self.history:
            return self.generationState.best

        # Находим поколение с минимальной задержкой у лучшей особи
        best_generation = min(self.history, key=lambda gen: gen.best.tardiness)
        return best_generation.best

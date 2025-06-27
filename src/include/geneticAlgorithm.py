from defaultClasses import ParamGeneticAlgorithm, ScheduleInfo, GenerationState, State, Task
from crossbreeding import CrossbreedingStrategy, SinglePointCrossbreeding
from mutation import MutationStrategy, NoMutation
from selection import SelectionStrategy, TournamentSelection
import random
from typing import List

class geneticAlgorithm:
    def __init__(self):
        self.params = ParamGeneticAlgorithm()
        self.iteration = 0 # generation_id
        self.selection : SelectionStrategy = TournamentSelection() # класс для отбора
        self.crossbreeding : CrossbreedingStrategy = SinglePointCrossbreeding()# класс для скрещиваний
        self.mutation : MutationStrategy = NoMutation()
        self.generationState = None 
        self.history = []
    
    def get_tasks(self, tasks : List[Task]):
        self.tasks = tasks
    
    def change_params(self, crossover, mutation, num_individuals, num_generations):
        self.params.crossover= crossover
        self.params.mutation = mutation
        self.params.num_individuals = num_individuals
        self.params.num_generations = num_generations
        self.params._validate()
    
    def create_individuals(self):
        population = []
        for i in range(self.params.num_individuals):
            order = [j for j in range(len(self.tasks))]
            random.shuffle(order)
            population.append(ScheduleInfo(order, self.tasks))
        self.generationState = GenerationState(population, state=State.INIT)
    
    def change_selection(self, new_selection):
        self.selection = new_selection
    
    def change_crossbreading(self, new_crossbreading):
        self.crossbreeding = new_crossbreading
    
    def do_selection(self):
        self.history.append(GenerationState)
        self.generationState = self.selection.select(self.generationState, self.params.num_to_select)
        
    def do_crossbreeding(self):
        self.history.append(self.generationState)
        self.generationState = self.crossbreeding.crossbreed(self.generationState, self.params.num_individuals, self.params.crossover)
    
    def do_mutation(self):
        self.history.append(GenerationState)
        self.generationState = self.mutation.mutate(self.generationState, self.params.mutation)
        self.iteration += 1

    def do_next(self):
        if(self.generationState.state == State.INIT):
            self.do_selection()
        elif (self.generationState.state == State.SELECTION):
            self.do_crossbreeding()
        elif (self.generationState.state == State.CROSSBREEDING):
            self.do_mutation()

    def go_back(self):
        if(self.generationState.id <= 1):
            raise ValueError("Impossible to move back!")
        self.generationState = self.history.pop()
        if(self.generationState.State == State.MUTATION):
            self.iteration -= 1
    
    def finish(self):
        while(self.generationState != State.MUTATION):
            self.do_next()
    
        for i in range(self.iteration, self.params.num_generations):
            self.do_selection()
            self.do_crossbreeding()
            self.do_mutation()
            
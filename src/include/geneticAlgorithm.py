from include.defaultClasses import ParamGeneticAlgorithm, ScheduleInfo, GenerationState
from include.tuiParser import tuiParser
import random

class geneticAlgorithm:
    def __init__(self):
        self.params = ParamGeneticAlgorithm()
        self.parser = tuiParser()
        self.generation_id = 0 # generation_id
        self.selection = None # класс для отбора
        self.crossbreeding = None # класс для скрещиваний и мутаций
        self.generationState = None
        self.history = []
    
    def read_tasks(self):
        self.tasks = self.parser.get_tasks()
    
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
        self.generationState = GenerationState(population)
        self.history.append(self.generationState)
    
from defaultClasses import ParamGeneticAlgorithm, ScheduleInfo
from tuiParser import tuiParser
import random

class geneticAlgorithm:
    def __init__(self):
        self.params = ParamGeneticAlgorithm()
        self.parser = tuiParser()
        self.generation_id = 0 # generation_id
        self.selection = None # класс для отбора
        self.crossbreeding = None # класс для скрещиваний и мутаций
    
    def read_tasks(self):
        self.tasks = self.parser.get_tasks()
    
    def change_params(self, crossover, mutation, num_individuals, num_generations):
        self.params.crossover= crossover
        self.params.mutation = mutation
        self.params.num_individuals = num_individuals
        self.params.num_generations = num_generations
        self.params._validate()
    
    def create_individuals(self):
        for i in range(self.params.num_individuals):
            random.shuffle(self.tasks)    
    
    
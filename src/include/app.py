from defaultClasses import ParamGeneticAlgorithm, ScheduleInfo
from parser import Parser

class App:
    def __init__(self):
        self.params = ParamGeneticAlgorithm()
        self.parser = Parser()
        self.tasks = self.parser.get_tasks()
        self.generation = 0 # текущая генерация
    
    def change_params(self, crossover, mutation, num_individuals, num_generations):
        self.params.crossover= crossover
        self.params.mutation = mutation
        self.params.num_individuals = num_individuals
        self.params.num_generations = num_generations
        self.params._validate()
    
    def create_generation(self):
        if(self.generation == 0):
            self.create_individuals()
    
    def create_individuals(self):
        pass
    
    
from defaultClasses import ParamGeneticAlgorithm, ScheduleInfo
from parser import Parser
import random

class geneticAlgorithm:
    def __init__(self):
        self.params = ParamGeneticAlgorithm()
        self.parser = Parser()
        self.tasks = self.parser.get_tasks() # должен быть список с тасками
        self.generation_id = 0 # текущая генерация
        self.current_generation = []
        self.selection = None
        self.crossbreeding = None
    
    def change_params(self, crossover, mutation, num_individuals, num_generations):
        self.params.crossover= crossover
        self.params.mutation = mutation
        self.params.num_individuals = num_individuals
        self.params.num_generations = num_generations
        self.params._validate()
    
    def create_individuals(self):
        for i in range(self.params.num_individuals):
            tasks.        
    
    
from defaultClasses import ScheduleInfo
from geneticAlgorithm import geneticAlgorithm
import tkinter as tk
from tkinter import ttk
from startState import StartState
from parser import Parser, RandomParser
from selection import *
from crossbreeding import *
from mutation import *

import random
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.parser = Parser()
        self.state = StartState(self.root, self)
        self.genAlgorithm = geneticAlgorithm()
        self.visual_settings()

    def change_seed(self, seed):
        random.seed(seed)

    def change_parser(self, parser):
        self.parser = parser

    def add_tasks(self, *args):
        tasks = self.parser.get_tasks(*args)
        self.genAlgorithm.set_tasks(tasks)
    
    def change_alg_params(self, *args):
        self.genAlgorithm.change_params(*args)
    
    def change_selection_type(self, type: str):
        if type == "TournamentSelection":
            self.genAlgorithm.selection = TournamentSelection()
        elif type == "RankSelection":
            self.genAlgorithm.selection = RankSelection()
        elif type == "StochasticUniversalSampling":
            self.genAlgorithm.selection = StochasticUniversalSampling()
    
    def change_crossbreeding_type(self, type: str):
        if type == "OrderCrossbreeding":
            self.genAlgorithm.crossbreeding = OrderCrossbreeding()
    
    def change_mutation_type(self, type: str):
        if type == "NoMutation":
            self.genAlgorithm.mutation = NoMutation()
        elif type == "SwapMutation":
            self.genAlgorithm.mutation = SwapMutation()
        elif type == "InversionMutation":
            self.genAlgorithm.mutation = InversionMutation()
    
    def visual_settings(self):
        self.root.geometry("1200x800")
        self.root.title("Генетический алгоритм")

    def run(self):
        self.state.run()
        self.root.mainloop()

    def clear_state(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def change_state(self, state):
        self.clear_state()
        self.state = state
        self.state.run()

import ttkbootstrap as ttkb
from geneticAlgorithm import geneticAlgorithm
from startState import StartState
from parser import Parser
from selection import *
from crossbreeding import *
from mutation import *
from tkinter import messagebox
import random


class App:
    def __init__(self):
        self.current_theme = "morph"
        self.root = ttkb.Window(themename="morph")
        self.parser = Parser()
        self.state = StartState(self.root, self)
        self.genAlgorithm = geneticAlgorithm()
        self.visual_settings()
        self.selection_type = "TournamentSelection"
        self.crossbreeding_type = "OrderCrossbreeding"
        self.mutation_type = "SwapMutation"

    def change_seed(self, seed):
        random.seed(seed)

    def change_parser(self, parser):
        self.parser = parser

    def add_tasks(self, *args):
        try:
            tasks = self.parser.get_tasks(*args)
            self.genAlgorithm.set_tasks(tasks)
        except Exception as e:
            message = str(e)
            self.show_error(message)

    def change_alg_params(self, *args):
        self.genAlgorithm.change_params(*args)

    def change_selection_type(self, type: str):
        if type == "TournamentSelection":
            self.genAlgorithm.selection = TournamentSelection()
        elif type == "RankSelection":
            self.genAlgorithm.selection = RankSelection()
        elif type == "StochasticUniversalSampling":
            self.genAlgorithm.selection = StochasticUniversalSampling()
        self.selection_type = type

    def change_crossbreeding_type(self, type: str):
        if type == "OrderCrossbreeding":
            self.genAlgorithm.crossbreeding = OrderCrossbreeding()
        self.crossbreeding_type = type

    def change_theme(self, theme_name):
        if theme_name != self.current_theme:
            self.current_theme = theme_name
            self.root.style.theme_use(theme_name)
            self.clear_state()
            self.state.run()

    def change_mutation_type(self, type: str):
        if type == "NoMutation":
            self.genAlgorithm.mutation = NoMutation()
        elif type == "SwapMutation":
            self.genAlgorithm.mutation = SwapMutation()
        elif type == "InversionMutation":
            self.genAlgorithm.mutation = InversionMutation()
        self.mutation_type = type

    def visual_settings(self):
        self.root.geometry("1200x1000")
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
    
    def show_error(self, message):
        messagebox.showerror("Ошибка!", message=message)

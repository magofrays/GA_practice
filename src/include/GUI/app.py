from defaultClasses import ScheduleInfo
from geneticAlgorithm import geneticAlgorithm
import tkinter as tk
from tkinter import ttk
from startState import StartState
from parser import Parser, RandomParser
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.parser = Parser()
        self.state = StartState(self.root, self)
        self.genAlgorithm = geneticAlgorithm()
        self.visual_settings()

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

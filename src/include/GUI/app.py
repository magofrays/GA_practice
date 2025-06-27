from defaultClasses import ScheduleInfo
from geneticAlgorithm import geneticAlgorithm
import tkinter as tk
from tkinter import ttk
from startState import StartState

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.parser = None
        self.state = StartState(self.root, self)
        self.genAlgorithm = geneticAlgorithm()
        self.visualSettings()

    def visualSettings(self):
        self.root.geometry("1200x800")
        self.root.title("Генетический алгоритм")

    def run(self):
        self.root.mainloop()


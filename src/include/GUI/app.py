from defaultClasses import ScheduleInfo
from geneticAlgorithm import geneticAlgorithm
import tkinter as tk
from startState import StartState

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.state = StartState(self.root)
        
        self.genAlgorithm = geneticAlgorithm()
        self.visualSettings()

    def visualSettings(self):
        self.root.geometry("1200x800")
        self.root.title("Генетический алгоритм")
        self.root.configure(bg="#404040")
    
    def run(self):
        self.root.mainloop()


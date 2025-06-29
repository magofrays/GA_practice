import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from graphs import AverageTardinessGUI
class GraphView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.iteration = self.app.genAlgorithm.iteration
        self.create_graph()

    def create_graph(self):
        self.averageTardiness = AverageTardinessGUI(self.app.genAlgorithm.history, self)
        self.iterationLabel = ttk.Label(self, text=f"Итерация: {self.iteration}/{self.app.genAlgorithm.params.num_generations}",
                                font = ("Arial", 12, "bold"))
        self.iterationLabel.pack(anchor="ne", fill=tk.BOTH, pady=10, padx=10)
    
    def update(self):
        self.averageTardiness.draw_graph()
        self.iteration = self.app.genAlgorithm.iteration
        self.iterationLabel.config(text=f"Итерация: {self.iteration}/{self.app.genAlgorithm.params.num_generations}")
    
    
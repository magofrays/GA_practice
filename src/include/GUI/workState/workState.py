import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from scheduleFrame import ScheduleFrame
from graphView import GraphView

class WorkState:
    def __init__(self, root, app):
        self.app = app
        self.root = root
        
    def run(self):
        self.main_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_window.pack(fill=tk.BOTH, expand=True)
        self.sched_frame = ScheduleFrame(self.main_window, self.app)
        self.graph_view = GraphView(self.main_window, self.app)
        self.main_window.add(self.sched_frame, weight=1)
        self.main_window.add(self.graph_view, weight=1)
        self.create_special_buttons()
    
    def create_special_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            button_frame, 
            text="В конец", 
            command=self.finish
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Следующий шаг", 
            command=self.do_next
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Предыдущий шаг", 
            command=self.go_back
        ).pack(side=tk.RIGHT, padx=5)
        
        
    
    def go_back(self):
        self.app.genAlgorithm.go_back()
        self.sched_frame.update()
        self.graph_view.update()
    
    def do_next(self):
        self.app.genAlgorithm.do_next()
        self.sched_frame.update()
        self.graph_view.update()
    
    def finish(self):
        self.app.genAlgorithm.finish()
        self.sched_frame.update()
        self.graph_view.update()


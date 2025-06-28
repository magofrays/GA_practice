import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from graphs import ImportTasksGUI
from settingsFrame import SettingsFrame
from importFrame import ImportFrame
from workState import WorkState

class StartState:
    def __init__(self, root, app):
        self.root = root
        self.app = app

    def run(self):
        self.main_window = ttk.PanedWindow(self.root)
        self.main_window.pack(fill=tk.BOTH, expand=True)
        self.inner_container = ttk.PanedWindow(self.main_window, orient=tk.HORIZONTAL)
        self.inner_container.pack(fill=tk.BOTH, expand=True)
        self.import_data = ImportFrame(self.inner_container, self.app, self)
        self.settings = SettingsFrame(self.inner_container, self.app)
        self.inner_container.add(self.import_data, weight=1)
        self.inner_container.add(self.settings, weight=1)
        self.main_window.add(self.inner_container, weight=2)
        self.create_graph()
        self.create_start_button()
    
    def create_graph(self):
        self.graph_container = ttk.Frame(self.main_window)
        self.graph = ImportTasksGUI(self.graph_container, [])
        self.main_window.add(self.graph_container, weight=1)
    
    def update_graph(self):
        tasks = self.app.genAlgorithm.tasks
        self.graph.update_tasks(tasks)
        
    def change_parent(self, parent):
        self.parent = parent

    def create_start_button(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Старт", 
            command=self.end
        ).pack(side=tk.RIGHT, padx=5)

    def end(self):
        print("Готово")
        self.app.genAlgorithm.create_individuals()
        self.app.change_state(WorkState(self.root, self.app))
        
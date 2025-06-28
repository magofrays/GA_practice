import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from graphs import ScheduleInfoGUI

class TaskSelection(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app


class TaskView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.update()

    
    def update(self):
        self.current_state = self.app.genAlgorithm.generationState
        self.scheduleInfo = ScheduleInfoGUI(self.current_state.best, self)

class TaskFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.task_view = TaskView(self.notebook, self.app)
        self.task_selection = TaskSelection(self.notebook, self.app)
        self.notebook.add(self.task_view, text="Просмотр задачи")
        self.notebook.add(self.task_selection, text="Выбор задачи для просмотра")
        
    
    
    
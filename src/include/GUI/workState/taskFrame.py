import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from graphs import ScheduleInfoGUI
from defaultClasses import State




class TaskView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.current_state = self.app.genAlgorithm.generationState
        self.header = ttk.Label(self, text=f"Тип: {self.get_type(self.current_state.state)}",
                           font = ("Arial", 12, "bold"))
        self.header.pack(pady=10, anchor="ne")
        self.scheduleInfo = ScheduleInfoGUI(self.current_state.best, self)

    def get_type(self, state : State):
        if state == State.SELECTION:
            return "Отбор"
        elif state == State.CROSSBREEDING:
            return "Скрещивание"
        elif state == State.MUTATION:
            return "Мутация"
        elif state == State.INIT:
            return "Создание"
        
    def update_task(self, task):
        self.task = task
        self.scheduleInfo.update_schedule(self.task)
        
    def update(self):
        self.current_state = self.app.genAlgorithm.generationState
        self.header.config(text=f"Тип: {self.get_type(self.current_state.state)}")
        self.update_task(self.current_state.best)
        
        

class TaskSelection(ttk.Frame):
    def __init__(self, parent, app, taskView):
        super().__init__(parent)
        self.app = app
        self.taskView = taskView
        

class TaskFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.task_view = TaskView(self.notebook, self.app)
        self.task_selection = TaskSelection(self.notebook, self.app, self.task_view)
        self.notebook.add(self.task_view, text="Просмотр задачи")
        self.notebook.add(self.task_selection, text="Выбор задачи для просмотра")
        
    
    
    
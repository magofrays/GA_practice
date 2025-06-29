import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from graphs import ScheduleInfoGUI
from defaultClasses import State

class ScheduleView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.current_state = self.app.genAlgorithm.generationState
        self.schedule = self.current_state.best
        self.create_gen_info()
        self.create_sched_info()
    
    def get_type(self, state : State):
        if state == State.SELECTION:
            return "Отбор"
        elif state == State.CROSSBREEDING:
            return "Скрещивание"
        elif state == State.MUTATION:
            return "Мутация"
        elif state == State.INIT:
            return "Создание"
    
    def create_gen_info(self):
        self.gen_info = ttk.Frame(self)
        self.gen_info.pack(fill=tk.BOTH, expand=True)
        self.gen_type = ttk.Label(self.gen_info, text=f"Тип: {self.get_type(self.current_state.state)}",
                           font = ("Arial", 12, "bold"))
        self.gen_type.pack(pady=10, padx=10, anchor="nw")
        self.gen_tardiness = ttk.Label(self.gen_info, text=f"Средняя задержка: {round(self.current_state.average_tardiness, 2)}",
                                font = ("Arial", 12, "bold"))
        self.gen_tardiness.pack(pady=10, padx=10, anchor="nw")
        self.gen_size = ttk.Label(self.gen_info, text=f"Количество особей: {len(self.current_state.population)}",
                                font = ("Arial", 12, "bold"))
        self.gen_size.pack(pady=10, padx=10, anchor="nw")
    
    def create_sched_info(self):
        self.sched_info = ttk.Frame(self)
        self.sched_info.pack(fill=tk.BOTH, expand=True)
        self.graph = ScheduleInfoGUI(self.current_state.best, self.sched_info)
        self.sched_id = ttk.Label(self.sched_info, text=f"ID расписания: {self.schedule.id}",
                           font = ("Arial", 12, "bold"))
        self.sched_id.pack(pady=10, padx=10, anchor="nw")
        self.sched_tardiness = ttk.Label(self.sched_info, text=f"Задержки расписания: {round(self.schedule.tardiness, 2)}",
                           font = ("Arial", 12, "bold"))
        self.sched_tardiness.pack(pady=10, padx=10, anchor="nw")
    
    def update_gen(self):
        self.current_state = self.app.genAlgorithm.generationState
        self.gen_type.config(text=f"Тип поколения: {self.get_type(self.current_state.state)}")
        self.gen_tardiness.config(text=f"Средняя задержка поколения: {round(self.current_state.average_tardiness, 2)}")
        self.gen_size.config(text=f"Количество особей в поколении: {len(self.current_state.population)}")

    def update_sched(self, schedule):
        self.schedule = schedule
        self.graph.update_schedule(self.schedule)
        self.sched_id.config(text=f"ID расписания: {self.schedule.id}")
        self.sched_tardiness.config(text=f"Задержки расписания: {round(self.schedule.tardiness, 2)}")
        
    def update(self):
        self.update_gen()
        self.update_sched(self.current_state.best)
        
        

class ScheduleSelection(ttk.Frame):
    def __init__(self, parent, app, taskView):
        super().__init__(parent)
        self.app = app
        self.taskView = taskView
    
    def update(self):
        pass
        

class ScheduleFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.schedule_view = ScheduleView(self.notebook, self.app)
        self.schedule_selection = ScheduleSelection(self.notebook, self.app, self.schedule_view)
        self.notebook.add(self.schedule_view, text="Просмотр расписания")
        self.notebook.add(self.schedule_selection, text="Выбор расписания для просмотра")
    
    def update(self):
        self.schedule_view.update()
        self.schedule_selection.update()
    
    
    
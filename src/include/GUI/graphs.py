from defaultClasses import ScheduleInfo, Task, GenerationState
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from itertools import cycle
import tkinter as tk
from tkinter import ttk
from typing import List

class AverageTardinessGUI:
    def __init__(self, history: List[GenerationState], root):
        self.root = root
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.history = history
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Расписание")
        self.ax.grid(False)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_graph()
    
    def draw_graph(self):
        self.ax.clear()
        self.ax.set_title("График средних задержек")
        self.ax.set_xlabel("Итерация")
        self.ax.set_ylabel("Средняя задержка")
        self.ax.grid(False)
        x = [element.id for element in self.history]
        y = [element.average_tardiness for element in self.history]
        
        self.ax.plot(x, y, 'o--', markersize=2, linewidth=1, color='b')
        self.canvas.draw()


class ScheduleInfoGUI:
    def __init__(self, scheduleInfo: ScheduleInfo, root):
        self.root = root
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.scheduleInfo = scheduleInfo
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Расписание")
        self.ax.grid(False)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        self.ax.set_title("Расписание")
        self.ax.grid(False)
        
        if not self.scheduleInfo.order:
            self.ax.text(0.5, 0.5, "Нет расписания", ha='center', va='center')
            self.canvas.draw()
            return
            
        tasks = self.scheduleInfo.tasks
        color_cycle = cycle(['red', 'blue', 'green', 'purple', 'orange'])
        
        curtime = 0
        for i in self.scheduleInfo.order:
            color = next(color_cycle)
            self.ax.plot(
                [curtime, curtime + tasks[i].time], 
                [0, 0], 
                color=color, 
                linewidth=4
            )
            curtime += tasks[i].time
        
        for i in self.scheduleInfo.order:
            self.ax.plot(
                [tasks[i].deadline, tasks[i].deadline], 
                [-0.1, 0.1],  
                color='red',
                linestyle='--',
                linewidth=1
            )
            
            self.ax.text(
                tasks[i].deadline, 
                -0.2,  
                f'ID: {tasks[i].id}',
                color='red',
                ha='center',
                va='top',
                fontsize=6
            )
        
        self.ax.set_ylim(-1, 1)
        self.canvas.draw()

    def update_schedule(self, new_schedule):
        """Обновляет расписание и перерисовывает график"""
        self.scheduleInfo = new_schedule
        self.draw_graph()

class ImportTasksGUI:
    def __init__(self, root, tasks):
        self.root = root
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.tasks = tasks
        self.ax = self.fig.add_subplot(111)
        self.color_cycle = cycle(['red', 'blue', 'green', 'purple', 'orange'])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_graph()

    def draw_graph(self):
        """Отрисовывает график на существующем canvas"""
        self.ax.clear()
        self.ax.set_title("Задачи дня")
        self.ax.grid(False)
        
        if not self.tasks:
            self.ax.text(0.5, 0.5, "Нет задач", ha='center', va='center')
            self.canvas.draw()
            return
            
        pos = 1
        size = len(self.tasks)
        step = 2 / size
        
        for task in self.tasks:
            color = next(self.color_cycle)
            # Отрисовка задачи
            self.ax.plot([0, task.time], [pos, pos], color=color, linewidth=4)
            
            # Отрисовка дедлайна
            self.ax.plot([task.deadline, task.deadline], 
                         [-0.05 + pos, 0.05 + pos],  
                         color='red',
                         linestyle='--',
                         linewidth=1)
            
            self.ax.text(task.deadline, -0.1 + pos, f'ID: {task.id}',
                         color='red', ha='center', va='top', fontsize=6)
            
            pos -= step
        
        self.ax.set_ylim(-1.2, 1.2)
        self.canvas.draw()

    def update_tasks(self, new_tasks):
        """Обновляет задачи и перерисовывает график"""
        self.tasks = new_tasks
        self.draw_graph()

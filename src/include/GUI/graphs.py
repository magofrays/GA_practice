from defaultClasses import ScheduleInfo, Task
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from itertools import cycle
import tkinter as tk
from tkinter import ttk
from typing import List

class ScheduleInfoGUI():
    def __init__(self, scheduleInfo: ScheduleInfo, root):
        self.root = root
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.scheduleInfo = scheduleInfo
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Расписание")
        self.ax.grid(False)
        
        # Создаем canvas один раз при инициализации
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Первоначальная отрисовка
        self.draw()

    def draw(self):
        """Отрисовывает график на существующем canvas"""
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
                linewidth=10
            )
            curtime += tasks[i].time
        
        for i in self.scheduleInfo.order:
            self.ax.plot(
                [tasks[i].deadline, tasks[i].deadline], 
                [-0.2, 0.2 ],  
                color='red',
                linestyle='--',
                linewidth=2
            )
            
            self.ax.text(
                tasks[i].deadline, 
                -0.3,  
                f'Deadline: {tasks[i].id}',
                color='red',
                ha='center',
                va='top',
                fontsize=8
            )
        
        self.ax.set_ylim(-1, 1)
        self.canvas.draw()

    def update_schedule(self, new_schedule):
        """Обновляет расписание и перерисовывает график"""
        self.scheduleInfo = new_schedule
        self.draw()

class ImportTasksGUI:
    def __init__(self, root, tasks):
        self.root = root
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.tasks = tasks
        self.ax = self.fig.add_subplot(111)
        self.color_cycle = cycle(['red', 'blue', 'green', 'purple', 'orange'])
        
        # Создаем canvas один раз при инициализации
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Первоначальная отрисовка
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
            
            self.ax.text(task.deadline, -0.1 + pos, f'Deadline: {task.id}',
                         color='red', ha='center', va='top', fontsize=8)
            
            pos -= step
        
        self.ax.set_ylim(-1.2, 1.2)
        self.canvas.draw()

    def update_tasks(self, new_tasks):
        """Обновляет задачи и перерисовывает график"""
        self.tasks = new_tasks
        self.draw_graph()

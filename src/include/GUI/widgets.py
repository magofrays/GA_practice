from defaultClasses import ScheduleInfo, Task
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from itertools import cycle
import tkinter as tk
from typing import List

class ScheduleInfoGUI():
    def __init__(self, scheduleInfo : ScheduleInfo, root):
        self.root = root
        self.fig = Figure(figsize=(5,3), dpi=100)
        self.scheduleInfo = scheduleInfo
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Расписание")
        self.ax.grid(False)

    
    def run(self):
        curtime = 0
        tasks = self.scheduleInfo.tasks
        color_cycle = cycle(['red', 'blue', 'green', 'purple', 'orange'])
        for i in self.scheduleInfo.order:
            self.ax.plot([curtime, curtime+tasks[i].time], [0, 0], color=next(color_cycle), linewidth=10)
            curtime += tasks[i].time
        for i in self.scheduleInfo.order:
            self.ax.plot(
                [tasks[i].deadline, tasks[i].deadline], 
                [-0.2, 0.2],  
                color='red',
                linestyle='--',
                linewidth=2
            )
            
            self.ax.text(
                tasks[i].deadline, 
                -0.3,  
                f'Deadline for tasks: {tasks[i].id}',
                color='red',
                ha='center',
                va='top'
            )
        self.ax.set_ylim(-1, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


class drawTasksGUI:
    def __init__(self, root, tasks : List[Task]):
        self.root = root
        self.fig = Figure(figsize=(5,3), dpi=100)
        self.tasks = tasks
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Задачи дня")
        self.ax.grid(False)
        self.color_cycle = cycle(['red', 'blue', 'green', 'purple', 'orange'])
    
    def run(self):
        self.ax.clear()
        pos = 1
        size = len(self.tasks) if len(self.tasks) > 0 else 1
        step = 2/size
        for task in self.tasks:
            self.ax.plot([0, task.time], [pos, pos], color=next(self.color_cycle), linewidth=10)
            self.ax.plot([task.deadline, task.deadline], 
                [-0.2+pos, 0.2+pos],  
                color='red',
                linestyle='--',
                linewidth=2
            )
            self.ax.text(
                task.deadline, 
                -0.3,  
                f'Deadline for tasks: {task.id}',
                color='red',
                ha='center',
                va='top'
            )
            pos -= step
        self.ax.set_ylim(-1.2, 1.2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_tasks(self, new_tasks):
        self.tasks = new_tasks
        self.run()

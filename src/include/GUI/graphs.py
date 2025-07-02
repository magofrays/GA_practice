from defaultClasses import ScheduleInfo, GenerationState
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from itertools import cycle
import tkinter as tk
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
        self.ax.set_ylabel("Задержки")
        self.ax.grid(False)
        x = [i for i in range(len(self.history))]
        y_mean = [element.average_tardiness for element in self.history]
        y_best = [element.best.tardiness for element in self.history]

        self.ax.plot(x, y_mean, 'o--', markersize=2, linewidth=1, color='b', label="Средние задержки")
        self.ax.plot(x, y_best, 'o--', markersize=2, linewidth=1, color='r', label="Лучшие задержки")
        self.ax.legend()
        self.canvas.draw()


class ScheduleInfoGUI:
    def __init__(self, scheduleInfo: ScheduleInfo, root):
        self.root = root
        self.fig = Figure(figsize=(5, 3), dpi=100)  # либо экспериментируем с размером, либо что-то другое думать
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

        if not self.scheduleInfo.order or not self.scheduleInfo.tasks:
            self.ax.text(0.5, 0.5, "Нет расписания", ha='center', va='center')
            self.canvas.draw()
            return

        # Динамическая высотка строки
        ROW_HEIGHT = 1.0

        active_ids = sorted(list(set(t.id for t in self.scheduleInfo.tasks)))
        num_active_tasks = len(active_ids)

        y_map: Dict[int, float] = {
            task_id: (num_active_tasks - 1 - i) * ROW_HEIGHT
            for i, task_id in enumerate(active_ids)
        }

        color_cycle = cycle(['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta'])
        color_map = {task_id: next(color_cycle) for task_id in active_ids}

        curtime = 0
        prev_y_pos = None

        for task_index in self.scheduleInfo.order:
            task = self.scheduleInfo.tasks[task_index]
            y_pos = y_map[task.id]

            start_time = curtime
            end_time = start_time + task.time

            if prev_y_pos is not None:
                self.ax.plot(
                    [start_time, start_time], [prev_y_pos, y_pos],
                    color='black', linestyle='--', linewidth=1, alpha=0.5  # Alpha чуть увеличен для видимости
                )

            self.ax.plot(
                [start_time, end_time], [y_pos, y_pos],
                color=color_map.get(task.id, 'gray'), linewidth=4
            )

            curtime = end_time
            prev_y_pos = y_pos

        for task in self.scheduleInfo.tasks:
            y_pos = y_map[task.id]
            self.ax.plot(
                [task.deadline, task.deadline], [y_pos - 0.2, y_pos + 0.2],
                color='red', linestyle='--', linewidth=1
            )
            self.ax.text(
                task.deadline, y_pos - 0.3, f'ID: {task.id}',
                color='red', ha='center', va='top', fontsize=7
            )

        self.ax.set_xlabel("Время")
        self.ax.set_ylabel("Задачи")

        if num_active_tasks > 0:
            y_labels = [f"ID {task_id}" for task_id in active_ids]
            y_ticks = [y_map[task_id] for task_id in active_ids]

            sorted_pairs = sorted(zip(y_ticks, y_labels), key=lambda pair: pair[0], reverse=True)
            final_ticks = [pair[0] for pair in sorted_pairs]
            final_labels = [pair[1] for pair in sorted_pairs]

            self.ax.set_yticks(final_ticks)
            self.ax.set_yticklabels(final_labels, fontsize=8)

            bottom_limit = -0.5 * ROW_HEIGHT
            top_limit = (num_active_tasks - 0.5) * ROW_HEIGHT
            self.ax.set_ylim(bottom_limit, top_limit)

        self.fig.set_constrained_layout(True)
        self.canvas.draw()

    def update_schedule(self, new_schedule):
        self.scheduleInfo = new_schedule
        self.draw_graph()


class ImportTasksGUI:
    def __init__(self, root, tasks):
        self.root = root
        self.fig = Figure(figsize=(5, 3), dpi=100)
        self.tasks = tasks
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        self.ax.set_title("Задачи дня")
        self.ax.grid(False)

        if not self.tasks:
            self.ax.text(0.5, 0.5, "Нет задач", ha='center', va='center')
            self.canvas.draw()
            return

        active_ids = sorted(list(set(t.id for t in self.tasks)))
        num_active_tasks = len(active_ids)

        y_map: Dict[int, int] = {
            task_id: num_active_tasks - 1 - i
            for i, task_id in enumerate(active_ids)
        }

        color_cycle = cycle(['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta'])
        color_map = {task_id: next(color_cycle) for task_id in active_ids}

        for task in self.tasks:
            y_pos = y_map[task.id]
            color = color_map.get(task.id, 'gray')

            self.ax.plot([0, task.time], [y_pos, y_pos], color=color, linewidth=4)

            self.ax.plot([task.deadline, task.deadline],
                         [y_pos - 0.2, y_pos + 0.2],
                         color='red',
                         linestyle='--',
                         linewidth=1)

            self.ax.text(task.deadline, y_pos - 0.3, f'ID: {task.id}',
                         color='red', ha='center', va='top', fontsize=7)

        self.ax.set_xlabel("Длительность / Дедлайн")
        self.ax.set_ylabel("Задачи")

        if num_active_tasks > 0:
            y_labels = [f"ID {task_id}" for task_id in active_ids]
            y_ticks = [y_map[task_id] for task_id in active_ids]

            sorted_pairs = sorted(zip(y_ticks, y_labels), key=lambda pair: pair[0], reverse=True)
            final_ticks = [pair[0] for pair in sorted_pairs]
            final_labels = [pair[1] for pair in sorted_pairs]

            self.ax.set_yticks(final_ticks)
            self.ax.set_yticklabels(final_labels, fontsize=8)
            self.ax.set_ylim(-1, num_active_tasks)

        self.fig.tight_layout()
        self.canvas.draw()

    def update_tasks(self, new_tasks):
        self.tasks = new_tasks
        self.draw_graph()

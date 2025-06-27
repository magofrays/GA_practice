from defaultClasses import ScheduleInfo
from geneticAlgorithm import geneticAlgorithm
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ScheduleInfoGUI():
    def __init__(self, scheduleInfo : ScheduleInfo, root):
        self.root = root
        self.fig = Figure(figsize=(5,3), dpi=100)
        self.scheduleInfo = ScheduleInfo
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Расписание")
        self.ax.grid(False)
    
    def run(self):
        curtime = 0
        tasks = self.scheduleInfo.tasks
        for i in self.scheduleInfo.order:
            self.ax.plot([curtime, 0], [curtime+tasks[i], 0], color="red", linewidth=10)
            curtime += tasks[i]
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.genAlgorithm = geneticAlgorithm()
        self.visualSettings()

    def visualSettings(self):
        self.root.geometry("1200x800")
        self.root.title("Генетический алгоритм")
        self.root.configure(bg="#404040")

    def run(self):
        self.genAlgorithm.read_tasks()
        self.genAlgorithm.create_individuals()
        best = self.genAlgorithm.generationState.best
        self.info = ScheduleInfoGUI(best, self.root)
        self.root.mainloop()

app = App()
app.run()
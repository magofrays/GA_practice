import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from graphs import ScheduleInfoGUI
from defaultClasses import State
import ttkbootstrap as ttkb

class ScheduleView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.current_state = self.app.genAlgorithm.generationState
        self.schedule = self.current_state.best
        self.create_gen_info()
        self.create_sched_info()
        self.create_graph()

    def get_type(self, state : State):
        if state == State.SELECTION:
            return "Отбор"
        elif state == State.CROSSBREEDING:
            return "Скрещивание"
        elif state == State.MUTATION:
            return "Мутация"
        elif state == State.INIT:
            return "Создание"
    
    def create_graph(self):
        self.graph_container = ttk.Frame(self)
        self.graph_container.pack(fill=tk.BOTH, expand=True)
        self.graph = ScheduleInfoGUI(self.current_state.best, self.graph_container)
        ttkb.Button(self.graph_container, text="Лучшее в поколении", command=self.best_gen_sched, bootstyle="info").pack(side=ttkb.RIGHT,
                                                                                                       padx=5)
        ttkb.Button(self.graph_container, text="Лучшее расписание", command=self.best_sched, bootstyle="info").pack(
            side=ttkb.RIGHT, padx=5)
    
    def create_gen_info(self):
        self.gen_info = ttk.Frame(self)
        self.gen_info.pack(fill=tk.X)
        self.gen_type = ttk.Label(self.gen_info, text=f"Тип: {self.get_type(self.current_state.state)}",
                           font = ("Arial", 12, "bold"))
        self.gen_type.pack(pady=10, padx=10, anchor="nw", side='left')
        self.gen_tardiness = ttk.Label(self.gen_info, text=f"Средняя задержка: {round(self.current_state.average_tardiness, 2)}",
                                font = ("Arial", 12, "bold"))
        self.gen_tardiness.pack(pady=10, padx=10, anchor="nw", side='left')
        self.gen_size = ttk.Label(self.gen_info, text=f"Количество особей: {len(self.current_state.population)}",
                                font = ("Arial", 12, "bold"))
        self.gen_size.pack(pady=10, padx=10, anchor="nw", side='left')
    
    def create_sched_info(self):
        self.sched_info = ttk.Frame(self)
        self.sched_info.pack(fill=tk.X)
        
        self.sched_id = ttk.Label(self.sched_info, text=f"ID расписания: {self.schedule.id}",
                           font = ("Arial", 12, "bold"))
        self.sched_id.pack(pady=10, padx=10, anchor="nw", side='left')
        self.sched_tardiness = ttk.Label(self.sched_info, text=f"Задержки расписания: {round(self.schedule.tardiness, 2)}",
                           font = ("Arial", 12, "bold"))
        self.sched_tardiness.pack(pady=10, padx=10, anchor="nw", side='left')
    
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

    def best_gen_sched(self):
        sched = self.current_state.best
        self.update_sched(sched)

    def best_sched(self):
        sched = self.app.genAlgorithm.get_best()
        self.update_sched(sched)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.setup_scrollable_frame()

    def setup_scrollable_frame(self):
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", tags="frame")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # ИСПРАВЛЕННАЯ ЧАСТЬ:
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        return "break"

    def clear(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # Принудительное обновление после очистки
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class ScheduleSelection(ttk.Frame):
    def __init__(self, parent, app, scheduleView: ScheduleView):
        self.style = ttk.Style()
    
        # Настройка стилей (фон, текст и т.д.)
        self.style.configure("a.TFrame", background="#9392e4")
        self.style.configure("a.TLabel", background="#9392e4", foreground="#2623bb")  # тот же фон
        
        self.style.configure("b.TFrame", background="#3432c9")  # светло-зелёный
        self.style.configure("b.TLabel", background="#3432c9", foreground="#000000")  # тот же
        super().__init__(parent)
        self.app = app
        self.schedView = scheduleView
        self.generationState = self.app.genAlgorithm.generationState
        self.scrollableFrame = ScrollableFrame(self)
        self.scrollableFrame.pack(fill="both", expand=True)
        self.create_sched_list()
        
    def create_sched_list(self):
        for sched in self.generationState.population:
            self.create_schedule_item(sched)
            
    def create_schedule_item(self, sched):
        """Создает интерактивный элемент расписания"""
        item_frame = ttk.Frame(
            self.scrollableFrame.scrollable_frame,
            padding=5,
            relief="solid",
            borderwidth=1,
        )
        item_frame.pack(fill="x", pady=2, padx=2)
        item_frame.configure(style='a.TFrame')
        name_label = ttk.Label(item_frame, text=f"Расписание: {sched.id}")
        name_label.pack(anchor="w")
        name_label.configure(style="a.TLabel")
        desc_label = ttk.Label(item_frame, text=f"Задержка: {sched.tardiness}")
        desc_label.pack(anchor="w")
        desc_label.configure(style="a.TLabel")
        self.style = ttk.Style()
        item_frame.bind("<Enter>", lambda e: self.change_styles(item_frame, name_label, desc_label, True))
        item_frame.bind("<Leave>", lambda e: self.change_styles(item_frame, name_label, desc_label, False))
        item_frame.bind("<Button-1>", lambda e, data=sched: self.change_sched_view(data))
    
    def change_styles(self, frame, name, desc, hower):
        if hower:
            frame.configure(style='b.TFrame')
            name.configure(style="b.TLabel")
            desc.configure(style="b.TLabel")
        else:
            frame.configure(style='a.TFrame')
            name.configure(style="a.TLabel")
            desc.configure(style="a.TLabel")
        
    
    def change_sched_view(self, sched):
        self.schedView.update_sched(sched)
        
    def update(self):
        self.scrollableFrame.clear()
        self.generationState = self.app.genAlgorithm.generationState
        self.create_sched_list()
        

class ScheduleFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.schedule_view = ScheduleView(self.notebook, self.app)
        # self.schedule_selection = ScheduleSelection(self.notebook, self.app, self.schedule_view)
        self.notebook.add(self.schedule_view, text="Просмотр расписания")
        # self.notebook.add(self.schedule_selection, text="Выбор расписания для просмотра")
    
    def update(self):
        self.schedule_view.update()
        # self.schedule_selection.update()
    
    
    
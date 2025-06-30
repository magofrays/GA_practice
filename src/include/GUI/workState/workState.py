import ttkbootstrap as ttkb
from scheduleFrame import ScheduleFrame
from graphView import GraphView


class WorkState:
    def __init__(self, root, app):
        self.app = app
        self.root = root

    def run(self):
        self.main_window = ttkb.PanedWindow(self.root, orient=ttkb.HORIZONTAL)
        self.main_window.pack(fill=ttkb.BOTH, expand=True)
        self.sched_frame = ScheduleFrame(self.main_window, self.app)
        self.graph_view = GraphView(self.main_window, self.app)
        self.main_window.add(self.sched_frame, weight=1)
        self.main_window.add(self.graph_view, weight=1)
        self.create_special_buttons()

    def create_special_buttons(self):
        button_frame = ttkb.Frame(self.root)
        button_frame.pack(fill=ttkb.X, padx=10, pady=10)

        # Добавляем стили к кнопкам
        ttkb.Button(button_frame, text="В конец", command=self.finish, bootstyle="primary").pack(side=ttkb.RIGHT,
                                                                                                 padx=5)
        ttkb.Button(button_frame, text="Следующий шаг", command=self.do_next, bootstyle="primary-outline").pack(
            side=ttkb.RIGHT, padx=5)
        ttkb.Button(button_frame, text="Предыдущий шаг", command=self.go_back, bootstyle="secondary-outline").pack(
            side=ttkb.RIGHT, padx=5)
        ttkb.Button(button_frame, text="В начало", command=self.go_to_start, bootstyle="info").pack(side=ttkb.RIGHT,
                                                                                                    padx=5)
        
    def go_to_start(self):
        from startState import StartState
        self.app.genAlgorithm.go_to_start()
        self.app.change_state(StartState(self.root, self.app))
    
    def go_back(self):
        self.app.genAlgorithm.go_back()
        self.sched_frame.update()
        self.graph_view.update()
    
    def do_next(self):
        self.app.genAlgorithm.do_next()
        self.sched_frame.update()
        self.graph_view.update()
    
    def finish(self):
        self.app.genAlgorithm.finish()
        self.sched_frame.update()
        self.graph_view.update()


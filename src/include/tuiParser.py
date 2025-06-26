from include.defaultClasses import Task
import sys

class tuiParser:
    def input_tasks(self):
        print("Вводите данные (Ctrl+D для завершения):")
        self.tasks = []
        for line in sys.stdin:
            time, deadline = line.strip().split()
            time, deadline = int(time), int(deadline)
            self.tasks.append(Task(time, deadline))

    def get_tasks(self):
        self.input_tasks()
        return self.tasks
        
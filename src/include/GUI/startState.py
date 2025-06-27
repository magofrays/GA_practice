import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from widgets import drawTasksGUI


class importFrame(ttk.Frame):
    def __init__(self, parent, state):
        super().__init__(parent)
        self.header = ttk.Label(self, text="Выбор источника данных",
                           font = ("Arial", 12, "bold"))
        self.state = state
        self.header.pack(pady=(0, 10), anchor="center") 
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.create_file_input()
        self.create_manual_input()
        self.create_random_input()
        
    def create_file_input(self):
        self.file_input = ttk.Frame(self.notebook)
        self.file_input.pack(fill=tk.BOTH, expand=True)
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(
            self.file_input, 
            textvariable=self.file_path_var,
            width=50,
            state='readonly'
        )
        self.file_path_entry.pack(padx=10, pady=10, fill=tk.X)
        select_button = ttk.Button(
            self.file_path_entry, 
            text="Выбрать файл",
            command=self.select_file
        )
        select_button.pack(anchor="ne")
        self.notebook.add(self.file_input, text="Из файла")

    def select_file(self):
        # меняем парсер
        file_types = [
            ('Текстовые файлы', '*.txt'),
            ('CSV файлы', '*.csv'),
        ]
        
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            initialdir="/home", 
            filetypes=file_types
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            file_path = self.file_path_var.get()


    def create_manual_input(self):
        self.manual_input = ttk.Frame(self.notebook)
        self.text_area = scrolledtext.ScrolledText(
            self.manual_input, 
            wrap=tk.WORD,
            font=("Arial", 8),
            padx=10,
            pady=10,
            height=20
        )
        
        self.text_area.pack(fill=tk.X, anchor="n", expand=True, padx=10, pady=10)
        self.notebook.add(self.manual_input, text="Ручной ввод")
        button_frame = ttk.Frame(self.manual_input)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="Готово", 
            command=self.read_input
        ).pack(side=tk.RIGHT, padx=5)
    
    def create_random_input(self):
        self.random_input = ttk.Frame(self.notebook)
        self.random_input.pack(fill=tk.BOTH, expand=True)
        self.notebook.add(self.random_input, text="Генерация данных")
        
    
    def read_input(self):
        pass

class settingsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Настройки", font=("Arial", 14)).pack(pady=10)
        content = ttk.Frame(self)
        content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        ttk.Button(content, text="Кнопка", command=lambda: print("Настройки")).pack(pady=20)

class graphContainer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.graph = drawTasksGUI(self, [])
        self.graph.run()
    
    def update(self, tasks):
        self.graph.update_tasks(tasks)

class StartState(ttk.PanedWindow):
    def __init__(self, root, app):
        super().__init__(root)
        self.app = app
        self.create_gui()

    
    def create_gui(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.inner_container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.inner_container.pack(fill=tk.BOTH, expand=True)
        self.left_window = importFrame(self.inner_container, self)
        self.right_window = settingsFrame(self.inner_container)
        self.inner_container.add(self.left_window, weight=1)
        self.inner_container.add(self.right_window, weight=1)
        self.down_window = graphContainer(self)
        self.add(self.inner_container, weight=2)  # 2/3 высоты
        self.add(self.down_window, weight=1)      # 1/3 высоты
    def change_parent(self, parent):
        self.parent = parent



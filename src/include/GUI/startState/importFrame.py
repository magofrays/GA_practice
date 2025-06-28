import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class ImportFrame(ttk.Frame):
    def __init__(self, parent, app, startState):
        super().__init__(parent)
        self.app = app
        self.startState = startState
        self.header = ttk.Label(self, text="Выбор источника данных",
                           font = ("Arial", 12, "bold"))
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
            tasks = self.app.parser.get_tasks(file_path)
            self.app.genAlgorithm.set_tasks(tasks)
            self.startState.update_graph()
            


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
        info = self.text_area.get("1.0", tk.END)
        info = info.strip()
        tasks = self.app.parser.get_tasks(info)
        self.app.genAlgorithm.set_tasks(tasks)
        self.startState.update_graph()
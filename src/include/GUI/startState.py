import tkinter as tk
from tkinter import ttk

class importFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.header = ttk.Label(self, text="Выбор источника данных",
                           font = ("Arrial", 12, "bold"))
        self.header.pack(pady=(0, 10), anchor="center") 
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 2. Создаем фреймы для каждой вкладки
        self.first_tab = ttk.Frame(self.notebook)
        self.second_tab = ttk.Frame(self.notebook)
        self.third_tab = ttk.Frame(self.notebook)
        
        # 3. Добавляем вкладки
        self.notebook.add(self.first_tab, text="Из файла")
        self.notebook.add(self.second_tab, text="Ручной ввод")
        self.notebook.add(self.third_tab, text="Third")

class settingsFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="", font=("Arial", 14)).pack(pady=10)
        content = ttk.Frame(self)
        content.pack(fill=tk.BOTH, expand=True)
        content.configure(style=f"{"black"}.TFrame")
        ttk.Button(content, text="Кнопка", command=lambda: print("black")).pack(pady=20)

class StartState:
    def __init__(self, root):
        self.root = root
        main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, 
                           sashwidth=8,  # Толщина разделителя
                           sashrelief=tk.SOLID,  # Стиль 3D
                           showhandle=True)  # Ручка для захвата
        main_paned.pack(fill=tk.BOTH, expand=True)
        self.left_window = importFrame(main_paned)
        self.right_window = settingsFrame(root)
        main_paned.add(self.left_window, width=300)
        main_paned.add(self.right_window, width=300)

    def change_root(self, root):
        self.root = root
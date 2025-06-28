import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class SettingLine(ttk.Frame):
    def __init__(self, parent, label, min_val, max_val, default, var_type=float):
        super().__init__(parent)
        self.var_type = var_type
        self.min_val = min_val
        self.max_val = max_val
        
        if var_type == int:
            self.value = tk.IntVar(value=default)
        else:
            self.value = tk.DoubleVar(value=default)
        
        ttk.Label(self, text=label, width=20, anchor="w").pack(side=tk.LEFT, padx=(0, 10))
        

        self.entry = ttk.Entry(self, width=8, textvariable=self.value)
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        
        self.slider = ttk.Scale(
            self, 
            from_=min_val, 
            to=max_val, 
            value=default,
            command=self.update_from_slider
        )
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.entry.bind("<FocusOut>", self.validate_entry)
        self.entry.bind("<Return>", self.validate_entry)
        self.value.trace_add("write", self.update_slider)
    
    def validate_entry(self, event=None):
        try:
            if self.var_type == int:
                val = int(self.entry.get())
            else:
                val = float(self.entry.get())
            
            if val < self.min_val:
                val = self.min_val
            elif val > self.max_val:
                val = self.max_val
            
            self.value.set(val)
        except ValueError:
            self.value.set(self.value.get())
    
    def update_from_slider(self, value):
        if self.var_type == int:
            self.value.set(int(float(value)))
        else:
            self.value.set(round(float(value), 2))
    
    def update_slider(self, *args):
        self.slider.config(value=self.value.get())


class SettingsNotebook(ttk.Notebook):
    def __init__(self, parent, settings_config):
        super().__init__(parent)
        self.settings = {}
        
        for tab_name, settings in settings_config.items():
            tab = ttk.Frame(self)
            self.add(tab, text=tab_name)
            self.create_tab_content(tab, settings)
    
    def create_tab_content(self, tab, settings):
        container = ttk.Frame(tab)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for i, (label, min_val, max_val, default, var_type) in enumerate(settings):
            setting = SettingLine(
                container, 
                label, 
                min_val, 
                max_val, 
                default,
                var_type
            )
            setting.pack(fill=tk.X, pady=5)
            
            key = label.lower().replace(" ", "_")
            self.settings[key] = setting.value
    
    def get_values(self):
        return {key: var.get() for key, var in self.settings.items()}


class SettingsFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.header = ttk.Label(self, text="Настройки приложения",
                           font = ("Arial", 12, "bold"))
        self.header.pack(pady=(0, 10), anchor="center")
        self.settings_config = {
            "Настройки алгоритма": [
                ("Размер популяции", 10, 500, 100, int),
                ("Количество поколений", 10, 1000, 100, int),
                ("Размер отбора", 10, 100, 50, int),
                ("Вероятность мутации", 0.0, 1.0, 0.5, float),
                ("Вероятность скрещивания", 0.0, 1.0, 0.5, float),
            ],
            "Настройки генерации": [
                ("Seed", 1, 10000, 1337, int),
            ],
            "Дополнительно": [
                ("Макс. время выполнения", 1, 600, 60, int),
                ("Порог сходимости", 0.001, 0.5, 0.01, float),
            ]
        }
        
        self.notebook = SettingsNotebook(self, self.settings_config)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Сохранить", 
            command=self.save_settings
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Сбросить", 
            command=self.reset_settings
        ).pack(side=tk.RIGHT, padx=5)
    
    def save_settings(self):
        settings = self.notebook.get_values()
        print("Сохраненные настройки:")
        for key, value in settings.items():
            print(f"{key}: {value}")
        
        tk.messagebox.showinfo("Настройки", "Настройки успешно сохранены!")
    
    def reset_settings(self):
        for tab_name, settings in self.settings_config.items():
            for setting in settings:
                key = setting[0].lower().replace(" ", "_")
                if key in self.notebook.settings:
                    self.notebook.settings[key].set(setting[3])
        
        tk.messagebox.showinfo("Настройки", "Настройки сброшены к значениям по умолчанию")

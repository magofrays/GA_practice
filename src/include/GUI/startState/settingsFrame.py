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
        
        # Главный контейнер для выравнивания
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.X, expand=True)
        
        # Метка слева
        ttk.Label(main_container, text=label, anchor="w").pack(side=tk.LEFT, padx=10)
        
        # Контейнер для правой части (поле + слайдер)
        right_container = ttk.Frame(main_container)
        right_container.pack(side=tk.RIGHT, padx=10)
        
        # Поле ввода
        self.entry = ttk.Entry(right_container, width=8, textvariable=self.value)
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Контейнер для слайдера с фиксированной шириной
        slider_container = ttk.Frame(right_container, width=200)
        slider_container.pack_propagate(False)
        slider_container.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        self.slider = ttk.Scale(
            slider_container, 
            from_=min_val, 
            to=max_val, 
            value=default,
            command=self.update_from_slider,
        )
        self.slider.pack(fill=tk.X, expand=True)
        
        # Привязка событий
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
    
    def get_value(self):
        return self.value.get()


class RangeSettingLine(ttk.Frame):
    def __init__(self, parent, label, value_range, default_range, var_type=int):
        super().__init__(parent)
        self.var_type = var_type
        self.min_val, self.max_val = value_range
        min_default, max_default = default_range
        
        # Основная метка
        ttk.Label(self, text=label, anchor="w").pack(side=tk.LEFT, padx=10)
        
        # Контейнер для элементов управления
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Создаем элементы для минимального и максимального значений
        self.min_setting = SettingLine(
            control_frame, 
            "Min:", 
            self.min_val, 
            self.max_val, 
            min_default, 
            var_type
        )
        self.min_setting.pack(fill=tk.X, expand=True)
        
        self.max_setting = SettingLine(
            control_frame, 
            "Max:", 
            self.min_val, 
            self.max_val, 
            max_default, 
            var_type
        )
        self.max_setting.pack(fill=tk.X, expand=True)
        
        # Связываем события для взаимной валидации
        self.min_setting.value.trace_add("write", self.validate_min)
        self.max_setting.value.trace_add("write", self.validate_max)
    
    def validate_min(self, *args):
        """Обеспечиваем, чтобы min ≤ max"""
        min_val = self.min_setting.value.get()
        max_val = self.max_setting.value.get()
        
        if min_val > max_val:
            self.max_setting.value.set(min_val)
    
    def validate_max(self, *args):
        """Обеспечиваем, чтобы max ≥ min"""
        min_val = self.min_setting.value.get()
        max_val = self.max_setting.value.get()
        
        if max_val < min_val:
            self.min_setting.value.set(max_val)
    
    def get_range(self):
        """Возвращает текущий диапазон значений"""
        return (
            self.min_setting.value.get(), 
            self.max_setting.value.get()
        )

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
            self.settings[label] = setting.value
    
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
        self.app.change_seed(settings["Seed"])
        self.app.change_alg_params(
            settings["Вероятность скрещивания"],
            settings["Вероятность мутации"],
            settings["Размер популяции"],
            settings["Количество поколений"],
            settings["Размер отбора"])
        messagebox.showinfo("Настройки", "Настройки успешно сохранены!")
    
    def reset_settings(self):
        for tab_name, settings in self.settings_config.items():
            for setting in settings:
                key = setting[0]
                if key in self.notebook.settings:
                    self.notebook.settings[key].set(setting[3])
        self.save_settings()
        messagebox.showinfo("Настройки", "Настройки сброшены к значениям по умолчанию")

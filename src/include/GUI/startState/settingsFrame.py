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
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.X, expand=True)
        ttk.Label(main_container, text=label, anchor="w").pack(side=tk.LEFT, padx=10)
        right_container = ttk.Frame(main_container)
        right_container.pack(side=tk.RIGHT, padx=10)
        self.entry = ttk.Entry(right_container, width=8, textvariable=self.value)
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
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
        
        ttk.Label(self, text=label, anchor="w").pack(side=tk.LEFT, padx=10)
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
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


class DropdownSetting(ttk.Frame):
    def __init__(self, parent, label, options, default=None):
        super().__init__(parent)
        self.options = options
        self.value = tk.StringVar(value=default if default else options[0])
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.X, expand=True)
        ttk.Label(main_container, text=label, anchor="w").pack(side=tk.LEFT, padx=10)
        right_container = ttk.Frame(main_container)
        right_container.pack(side=tk.RIGHT, padx=10)
        self.dropdown = ttk.Combobox(
            right_container,
            textvariable=self.value,
            values=options,
            state="readonly",
            width=15
        )
        self.dropdown.pack(side=tk.LEFT, padx=10)
        if default and default in options:
            self.value.set(default)
        else:
            self.value.set(options[0])
    
    def get_value(self):
        return self.value.get()
    
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
        self.settings_notebook = ttk.Notebook(self)
        self.settings_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.settings_tabs = {}
        self.settings = {}
        for tab_name, settings in self.settings_config.items():
            tab = ttk.Frame(self)
            self.settings_notebook.add(tab, text=tab_name)
            self.create_tab_content(tab, settings)
            self.settings_tabs[tab_name] = tab
        
        alg_settings = self.settings_tabs["Настройки алгоритма"]
        selection_type = DropdownSetting(alg_settings, "Тип отбора", ["TournamentSelection", "RankSelection", "StochasticUniversalSampling"], "TournamentSelection")
        selection_type.pack(anchor="nw", fill=tk.BOTH, pady=5)
        self.settings["Тип отбора"] = selection_type
        crossbreeding_type = DropdownSetting(alg_settings, "Тип скрещивания", ["OrderCrossbreeding"], "OrderCrossbreeding")
        crossbreeding_type.pack(anchor="nw", fill=tk.BOTH, pady=5)
        self.settings["Тип скрещивания"] = selection_type
        mutation_type = DropdownSetting(alg_settings, "Тип мутации", ["NoMutation", "SwapMutation", "InversionMutation"], "SwapMutation")
        mutation_type.pack(anchor="nw", fill=tk.BOTH, pady=5)
        self.settings["Тип мутации"] = selection_type
        self.create_buttons()
        
    def create_buttons(self):
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
    
    def create_tab_content(self, tab, settings):
        for i, (label, min_val, max_val, default, var_type) in enumerate(settings):
            setting = SettingLine(
                tab, 
                label, 
                min_val, 
                max_val, 
                default,
                var_type
            )
            setting.pack(fill=tk.X, pady=5)
            self.settings[label] = setting
        
    def get_values(self):
        return {key: var.get_value() for key, var in self.settings.items()}
    
    def save_settings(self):
        settings = self.get_values()
        self.app.change_seed(settings["Seed"])
        self.app.change_alg_params(
            settings["Вероятность скрещивания"],
            settings["Вероятность мутации"],
            settings["Размер популяции"],
            settings["Количество поколений"],
            settings["Размер отбора"])
        self.app.change_selection_type(settings["Тип отбора"])
        self.app.change_crossbreeding_type(settings["Тип скрещивания"])
        self.app.change_mutation_type(settings["Тип мутации"])
        messagebox.showinfo("Настройки", "Настройки успешно сохранены!")
    
    def reset_settings(self):
        for tab_name, settings in self.settings_config.items():
            for setting in settings:
                key = setting[0]
                if key in self.settings:
                    self.settings[key].set(setting[3])
        messagebox.showinfo("Настройки", "Настройки сброшены к значениям по умолчанию")
        self.save_settings()
        

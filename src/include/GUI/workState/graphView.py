import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class GraphView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
    
    
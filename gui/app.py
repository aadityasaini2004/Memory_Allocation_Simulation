import tkinter as tk
import tkinter.ttk as ttk
from core.allocator import MemoryAllocator
from gui.styles import setup_theme
from gui.simulator_view import SimulatorView
from gui.comparison_view import ComparisonView
from gui.learning_view import LearningView

class MemorySimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memory Allocation Simulator")
        self.geometry("1050x700")
        self.minsize(900, 650)
        
        setup_theme(self)
        self.configure(bg="#121417")
        
        self.allocator = MemoryAllocator(1024)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.sim_tab = SimulatorView(self.notebook, self.allocator)
        self.notebook.add(self.sim_tab, text="Simulator")
        
        self.comp_tab = ComparisonView(self.notebook)
        self.notebook.add(self.comp_tab, text="Algorithm Comparison")
        
        self.learn_tab = LearningView(self.notebook)
        self.notebook.add(self.learn_tab, text="Learning Center")
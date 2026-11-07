import tkinter as tk
import tkinter.ttk as ttk
from core.models import Process
from typing import List

class ProcessTable(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Panel.TFrame")
        
        ttk.Label(self, text="Active Processes", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        columns = ("pid", "start", "end", "size")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        
        self.tree.heading("pid", text="Process ID")
        self.tree.heading("start", text="Start Address")
        self.tree.heading("end", text="End (Exclusive)")
        self.tree.heading("size", text="Size (KB)")
        
        self.tree.column("pid", width=100)
        self.tree.column("start", width=100)
        self.tree.column("end", width=100)
        self.tree.column("size", width=100)
        
        self.tree.pack(fill="both", expand=True)

    def update_table(self, processes: List[Process]):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        sorted_processes = sorted(processes, key=lambda p: p.start)
        for p in sorted_processes:
            self.tree.insert("", "end", values=(p.process_id, p.start, p.end, p.size))
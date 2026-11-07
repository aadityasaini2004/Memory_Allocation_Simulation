import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

class ActivityLog(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Panel.TFrame")
        
        ttk.Label(self, text="Activity Log", style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        
        columns = ("time", "action", "details")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("time", text="Time")
        self.tree.heading("action", text="Action")
        self.tree.heading("details", text="Details")
        
        self.tree.column("time", width=70, stretch=False)
        self.tree.column("action", width=120, stretch=False)
        self.tree.column("details", width=250, stretch=True)
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def log_event(self, action: str, details: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Insert at index 0 so newest events appear at the top
        self.tree.insert("", "0", values=(timestamp, action, details))
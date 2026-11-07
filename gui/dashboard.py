import tkinter as tk
import tkinter.ttk as ttk
from typing import Dict, Any

class Dashboard(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Panel.TFrame")
        self.cards = {}
        
        metrics = [
            ("total_memory", "Total Memory (KB)"),
            ("used_memory", "Used Memory (KB)"),
            ("free_memory", "Free Memory (KB)"),
            ("utilization", "Utilization (%)"),
            ("largest_free_block", "Largest Free (KB)"),
            ("free_hole_count", "Free Holes"),
            ("active_process_count", "Active Processes"),
            ("external_fragmentation", "Ext. Fragmentation")
        ]
        
        for i, (key, title) in enumerate(metrics):
            card = ttk.Frame(self, style="Card.TFrame", padding=10)
            card.grid(row=i//4, column=i%4, padx=5, pady=5, sticky="nsew")
            self.columnconfigure(i%4, weight=1)
            
            ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
            val_label = ttk.Label(card, text="0", style="CardValue.TLabel")
            val_label.pack(anchor="w", pady=(5, 0))
            self.cards[key] = val_label

    def update_metrics(self, metrics: Dict[str, Any]):
        for key, val_label in self.cards.items():
            val = metrics.get(key, "0")
            if isinstance(val, float):
                val_label.config(text=f"{val:.2f}")
            elif val == "N/A":
                val_label.config(text="N/A")
            else:
                val_label.config(text=str(val))
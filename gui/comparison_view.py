import tkinter as tk
import tkinter.ttk as ttk
from core.models import AllocationAlgorithm
from core.comparison import run_comparison
from core.scenarios import setup_demo_scenario

class ComparisonView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Panel.TFrame")
        
        # Header
        header_frame = ttk.Frame(self, padding=10)
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="Algorithm Comparison", style="Header.TLabel").pack(side="left")
        ttk.Button(header_frame, text="Run Demo Comparison", style="Accent.TButton", command=self._run_demo).pack(side="right")
        
        # Description
        desc = ("This runs an isolated comparison using the demo scenario (1024 KB). "
                "It sets up P1-P5, frees P2 and P4, and then attempts to allocate P6 (140 KB) and P7 (180 KB) "
                "under all three algorithms to observe how fragmentation diverges.")
        ttk.Label(self, text=desc, wraplength=900).pack(fill="x", padx=15, pady=5)
        
        # Results Container
        self.results_frame = ttk.Frame(self)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for i in range(3):
            self.results_frame.columnconfigure(i, weight=1)
            
        self.result_panels = {}

    def _run_demo(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        operations = [("P6", 140), ("P7", 180)]
        results = run_comparison(1024, setup_demo_scenario, operations)
        
        algos = [AllocationAlgorithm.FIRST_FIT, AllocationAlgorithm.BEST_FIT, AllocationAlgorithm.WORST_FIT]
        
        for i, algo in enumerate(algos):
            data = results[algo]
            metrics = data["metrics"]
            holes = data["free_holes"]
            
            panel = ttk.Frame(self.results_frame, style="Card.TFrame", padding=15)
            panel.grid(row=0, column=i, sticky="nsew", padx=5)
            
            ttk.Label(panel, text=algo.value, style="Header.TLabel").pack(anchor="w", pady=(0, 10))
            
            # Formatted metrics display
            self._add_metric_row(panel, "Total Used:", f"{metrics['used_memory']} KB")
            self._add_metric_row(panel, "Total Free:", f"{metrics['free_memory']} KB")
            self._add_metric_row(panel, "Largest Hole:", f"{metrics['largest_free_block']} KB")
            
            frag_val = metrics['external_fragmentation']
            frag_str = f"{frag_val:.2f}%" if isinstance(frag_val, float) else str(frag_val)
            self._add_metric_row(panel, "Fragmentation:", frag_str)
            
            ttk.Separator(panel, orient="horizontal").pack(fill="x", pady=10)
            
            ttk.Label(panel, text="Final Free Holes (Order):", style="CardTitle.TLabel").pack(anchor="w")
            holes_str = ", ".join(f"{h} KB" for h in holes) if holes else "None"
            ttk.Label(panel, text=holes_str, wraplength=250).pack(anchor="w", pady=(5, 10))

    def _add_metric_row(self, parent, label, value):
        row = ttk.Frame(parent, style="Card.TFrame")
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label).pack(side="left")
        ttk.Label(row, text=value, font=("Segoe UI", 10, "bold")).pack(side="right")
import tkinter as tk
import tkinter.ttk as ttk
from core.models import AllocationAlgorithm
from core.exceptions import MemorySimulatorError

class ProcessPanel(ttk.Frame):
    def __init__(self, parent, allocate_cb, deallocate_cb):
        super().__init__(parent, style="Panel.TFrame", padding=15)
        
        self.allocate_cb = allocate_cb
        self.deallocate_cb = deallocate_cb
        
        ttk.Label(self, text="Process Control", style="Header.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Allocate Section
        ttk.Label(self, text="Process ID:", style="Panel.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_pid = ttk.Entry(self, width=15)
        self.entry_pid.grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(self, text="Size (KB):", style="Panel.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_size = ttk.Entry(self, width=15)
        self.entry_size.grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Label(self, text="Algorithm:", style="Panel.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        self.algo_var = tk.StringVar(value=AllocationAlgorithm.FIRST_FIT.value)
        self.combo_algo = ttk.Combobox(self, textvariable=self.algo_var, values=[e.value for e in AllocationAlgorithm], state="readonly", width=13)
        self.combo_algo.grid(row=3, column=1, sticky="w", pady=5)
        
        self.btn_allocate = ttk.Button(self, text="Allocate", style="Accent.TButton", command=self._handle_allocate)
        self.btn_allocate.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(15, 10))
        
        ttk.Separator(self, orient="horizontal").grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Deallocate Section
        ttk.Label(self, text="Process ID to free:", style="Panel.TLabel").grid(row=6, column=0, sticky="w", pady=5)
        self.entry_dealloc_pid = ttk.Entry(self, width=15)
        self.entry_dealloc_pid.grid(row=6, column=1, sticky="w", pady=5)
        
        self.btn_deallocate = ttk.Button(self, text="Deallocate", command=self._handle_deallocate)
        self.btn_deallocate.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(15, 10))

        # Error Label
        self.lbl_error = ttk.Label(self, text="", style="Error.TLabel", wraplength=200)
        self.lbl_error.grid(row=8, column=0, columnspan=2, sticky="w", pady=10)

    def show_error(self, msg):
        self.lbl_error.config(text=msg)

    def clear_error(self):
        self.lbl_error.config(text="")

    def _handle_allocate(self):
        self.clear_error()
        pid = self.entry_pid.get().strip()
        size_str = self.entry_size.get().strip()
        algo_str = self.algo_var.get()
        
        if not pid:
            self.show_error("Process ID cannot be empty.")
            return
        if not size_str.isdigit() or int(size_str) <= 0:
            self.show_error("Size must be a positive integer.")
            return
        
        algo = AllocationAlgorithm(algo_str)
        try:
            self.allocate_cb(pid, int(size_str), algo)
            self.entry_pid.delete(0, tk.END)
            self.entry_size.delete(0, tk.END)
        except MemorySimulatorError as e:
            self.show_error(str(e))

    def _handle_deallocate(self):
        self.clear_error()
        pid = self.entry_dealloc_pid.get().strip()
        if not pid:
            self.show_error("Process ID cannot be empty.")
            return
        
        try:
            self.deallocate_cb(pid)
            self.entry_dealloc_pid.delete(0, tk.END)
        except MemorySimulatorError as e:
            self.show_error(str(e))
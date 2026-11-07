import tkinter as tk
import tkinter.ttk as ttk
from core.allocator import MemoryAllocator
from core.memory_metrics import calculate_metrics
from core.scenarios import setup_demo_scenario
from gui.process_panel import ProcessPanel
from gui.process_table import ProcessTable
from gui.dashboard import Dashboard
from gui.memory_visualizer import MemoryVisualizer
from gui.activity_log import ActivityLog

class SimulatorView(ttk.Frame):
    def __init__(self, parent, allocator: MemoryAllocator):
        super().__init__(parent)
        self.allocator = allocator
        
        self.columnconfigure(1, weight=3) # Give right side (map/table) more space
        self.rowconfigure(1, weight=1)
        
        # Header Bar
        header_frame = ttk.Frame(self, padding=10)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        ttk.Label(header_frame, text="Memory Allocation Simulator", style="Header.TLabel").pack(side="left")
        
        ttk.Button(header_frame, text="Load Demo Scenario", command=self._load_demo).pack(side="right", padx=5)
        ttk.Button(header_frame, text="Reset", command=self._reset_sim).pack(side="right", padx=5)
        
        ttk.Label(header_frame, text="Total Memory (KB):").pack(side="right", padx=5)
        self.entry_total_mem = ttk.Entry(header_frame, width=10)
        self.entry_total_mem.insert(0, "1024")
        self.entry_total_mem.pack(side="right", padx=5)

        # Left Panel (Controls + Log)
        left_frame = ttk.Frame(self)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        self.process_panel = ProcessPanel(left_frame, self._allocate, self._deallocate)
        self.process_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.activity_log = ActivityLog(left_frame)
        self.activity_log.grid(row=1, column=0, sticky="nsew")

        # Right Panel (Dashboard + Visualizer + Table)
        right_frame = ttk.Frame(self)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=10)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)

        self.dashboard = Dashboard(right_frame)
        self.dashboard.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.visualizer = MemoryVisualizer(right_frame)
        self.visualizer.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        self.process_table = ProcessTable(right_frame)
        self.process_table.grid(row=2, column=0, sticky="nsew")

        self.activity_log.log_event("System", f"Simulation initialized with {self.allocator._total_memory} KB")
        self.refresh_views()

    def _allocate(self, pid, size, algo):
        try:
            self.allocator.allocate(pid, size, algo)
            self.activity_log.log_event("Allocate Success", f"[{algo.value}] {pid} allocated {size} KB")
            self.refresh_views()
        except Exception as e:
            self.activity_log.log_event("Allocate Failed", f"{pid} ({size} KB): {str(e)}")
            raise e # re-raise so the process_panel can show it

    def _deallocate(self, pid):
        try:
            self.allocator.deallocate(pid)
            self.activity_log.log_event("Deallocate Success", f"Freed process {pid}")
            self.refresh_views()
        except Exception as e:
            self.activity_log.log_event("Deallocate Failed", f"{pid}: {str(e)}")
            raise e
        
    def _reset_sim(self):
        self.process_panel.clear_error()
        try:
            mem_str = self.entry_total_mem.get().strip()
            if not mem_str.isdigit() or int(mem_str) <= 0:
                self.process_panel.show_error("Invalid total memory for reset.")
                return
            self.allocator.reset(int(mem_str))
            self.activity_log.log_event("Reset", f"Memory reset to {mem_str} KB")
            self.refresh_views()
        except Exception as e:
            self.process_panel.show_error(str(e))
            
    def _load_demo(self):
        self.process_panel.clear_error()
        setup_demo_scenario(self.allocator)
        self.entry_total_mem.delete(0, tk.END)
        self.entry_total_mem.insert(0, "1024")
        self.activity_log.log_event("Demo Loaded", "Loaded 1024 KB fragmentation scenario")
        self.refresh_views()
        
    def refresh_views(self):
        segments = self.allocator.get_segments()
        processes = self.allocator.get_processes()
        total_mem = self.allocator._total_memory
        metrics = calculate_metrics(total_mem, segments, processes)
        
        self.dashboard.update_metrics(metrics)
        self.visualizer.update_map(segments, total_mem)
        self.process_table.update_table(processes)
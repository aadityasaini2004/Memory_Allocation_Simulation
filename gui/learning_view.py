import tkinter as tk
import tkinter.ttk as ttk

class LearningView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Panel.TFrame")
        
        ttk.Label(self, text="Learning Center", style="Header.TLabel").pack(anchor="w", padx=15, pady=(15, 5))
        
        text_widget = tk.Text(self, wrap="word", bg="#1B1F24", fg="#F5F7FA", font=("Segoe UI", 11), borderwidth=0, highlightthickness=0)
        text_widget.pack(fill="both", expand=True, padx=15, pady=10)
        
        content = """
1. Contiguous Memory Allocation
In this model, each process is loaded into a single, continuous block of memory. The simulator uses variable-sized partitions, meaning the memory is not divided into fixed chunks ahead of time. Instead, processes are given exactly the size they request, and holes are created dynamically.

2. Allocation Algorithms (Time Complexity: O(n))
When a process requests memory, the OS must find a suitable free hole:
• First Fit: Scans memory from address 0 and selects the very first free hole that is large enough. It is generally fast but can leave small, unusable holes at the beginning of memory.
• Best Fit: Scans all free holes and selects the smallest hole that is large enough. This preserves larger holes for future requests but tends to create tiny, useless remainder holes (slivers).
• Worst Fit: Scans all free holes and selects the largest available hole. The idea is that the remainder of the hole will still be large enough to be useful for another process.

3. Splitting and Coalescing
• Splitting: When an algorithm selects a free hole that is larger than the requested size, the hole is split. The process takes the space it needs from the start of the hole, and the remainder becomes a new, smaller free hole.
• Coalescing: When a process is deallocated, its memory becomes a free hole. If this new hole is directly adjacent to other free holes (on the left, right, or both), the OS automatically merges (coalesces) them into a single, larger free hole.

4. External Fragmentation
External fragmentation occurs when the total free memory in the system is sufficient to satisfy a request, but the request still fails because the free memory is scattered in non-contiguous holes, none of which is large enough individually.

Educational Metric Formula:
External Fragmentation = (1 - (Largest Free Block / Total Free Memory)) * 100

*Note: This formula is an educational indicator used in this simulator to demonstrate the severity of fragmentation. A value of 0% means all free memory is in one block. Higher percentages indicate the free memory is heavily fractured.*
"""
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled") # Make read-only
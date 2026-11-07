import tkinter as tk
import tkinter.ttk as ttk
from typing import List
from core.models import MemorySegment
from gui.styles import Colors

class MemoryVisualizer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Panel.TFrame")
        
        # Legend & Header
        top_frame = ttk.Frame(self, style="Panel.TFrame")
        top_frame.pack(fill="x", pady=(0, 5))
        
        ttk.Label(top_frame, text="Memory Map", style="Subheader.TLabel").pack(side="left")
        
        legend_free = tk.Label(top_frame, text="   ", bg=Colors.FREE)
        legend_free.pack(side="right", padx=(5, 0))
        ttk.Label(top_frame, text="Free").pack(side="right")
        
        legend_alloc = tk.Label(top_frame, text="   ", bg=Colors.ALLOCATED)
        legend_alloc.pack(side="right", padx=(15, 0))
        ttk.Label(top_frame, text="Allocated").pack(side="right")

        # Canvas Map
        self.canvas = tk.Canvas(self, height=60, bg=Colors.BG_SECONDARY, highlightthickness=0)
        self.canvas.pack(fill="x", expand=False, pady=5)
        
        # Hover Details
        self.hover_label = ttk.Label(self, text="Hover over a segment to see details.", style="CardTitle.TLabel")
        self.hover_label.pack(anchor="w")

        # Bindings
        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Leave>", self._on_mouse_leave)
        
        self._current_segments = []
        self._current_total = 1024
        self._rects = []

    def update_map(self, segments: List[MemorySegment], total_memory: int):
        self._current_segments = segments
        self._current_total = total_memory
        self._draw()
        
    def _on_resize(self, event):
        self._draw()
        
    def _draw(self):
        self.canvas.delete("all")
        self._rects.clear()
        
        if not self._current_segments or self._current_total <= 0:
            return
            
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1: 
            return # Canvas hasn't rendered its layout yet
            
        x_offset = 0
        for seg in self._current_segments:
            seg_width = (seg.size / self._current_total) * width
            color = Colors.FREE if seg.is_free else Colors.ALLOCATED
            
            # Draw segment block
            self.canvas.create_rectangle(x_offset, 0, x_offset + seg_width, height, 
                                         fill=color, outline=Colors.BORDER, width=1)
            self._rects.append((x_offset, x_offset + seg_width, seg))
            
            # Draw label if block is wide enough
            if seg_width > 40:
                text = "FREE" if seg.is_free else seg.process_id
                self.canvas.create_text(x_offset + seg_width/2, height/2, text=text, fill=Colors.BG_MAIN, font=("Segoe UI", 9, "bold"))
            
            x_offset += seg_width

    def _on_mouse_move(self, event):
        x = event.x
        for x_start, x_end, seg in self._rects:
            if x_start <= x <= x_end:
                status = "Free Segment" if seg.is_free else f"Process {seg.process_id}"
                self.hover_label.config(text=f"{status}  |  Range: [{seg.start}, {seg.end})  |  Size: {seg.size} KB")
                return
        self.hover_label.config(text="Hover over a segment to see details.")
        
    def _on_mouse_leave(self, event):
        self.hover_label.config(text="Hover over a segment to see details.")
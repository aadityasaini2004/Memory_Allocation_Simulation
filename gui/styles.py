import tkinter.ttk as ttk

class Colors:
    BG_MAIN = "#121417"
    BG_PANEL = "#1B1F24"
    BG_SECONDARY = "#252B32"
    TEXT_PRIMARY = "#F5F7FA"
    TEXT_SECONDARY = "#AAB3BD"
    ACCENT = "#3B82F6"
    ERROR = "#EF4444"
    ALLOCATED = "#22C55E"
    FREE = "#FACC15"
    BORDER = "#343B44"

def setup_theme(root):
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    
    # Configure Base
    style.configure(".", 
                    background=Colors.BG_MAIN, 
                    foreground=Colors.TEXT_PRIMARY,
                    troughcolor=Colors.BG_SECONDARY,
                    selectbackground=Colors.ACCENT,
                    selectforeground=Colors.TEXT_PRIMARY,
                    font=("Segoe UI", 10))
                    
    # Frames
    style.configure("TFrame", background=Colors.BG_MAIN)
    style.configure("Panel.TFrame", background=Colors.BG_PANEL)
    style.configure("Card.TFrame", background=Colors.BG_SECONDARY, borderwidth=1, relief="solid", bordercolor=Colors.BORDER)
    
    # Labels
    style.configure("TLabel", background=Colors.BG_MAIN, foreground=Colors.TEXT_PRIMARY)
    style.configure("Panel.TLabel", background=Colors.BG_PANEL, foreground=Colors.TEXT_PRIMARY)
    style.configure("Header.TLabel", background=Colors.BG_MAIN, foreground=Colors.TEXT_PRIMARY, font=("Segoe UI", 16, "bold"))
    style.configure("Subheader.TLabel", background=Colors.BG_MAIN, foreground=Colors.TEXT_SECONDARY, font=("Segoe UI", 12))
    style.configure("CardValue.TLabel", background=Colors.BG_SECONDARY, foreground=Colors.TEXT_PRIMARY, font=("Segoe UI", 14, "bold"))
    style.configure("CardTitle.TLabel", background=Colors.BG_SECONDARY, foreground=Colors.TEXT_SECONDARY, font=("Segoe UI", 9))
    style.configure("Error.TLabel", foreground=Colors.ERROR, background=Colors.BG_PANEL)

    # Buttons
    style.configure("TButton", background=Colors.BG_SECONDARY, foreground=Colors.TEXT_PRIMARY, borderwidth=1, focuscolor=Colors.ACCENT)
    style.map("TButton", background=[("active", Colors.ACCENT)])
    style.configure("Accent.TButton", background=Colors.ACCENT, foreground=Colors.TEXT_PRIMARY, font=("Segoe UI", 10, "bold"))
    style.map("Accent.TButton", background=[("active", "#2563EB")])

    # Treeview (Process Table)
    style.configure("Treeview", background=Colors.BG_SECONDARY, fieldbackground=Colors.BG_SECONDARY, foreground=Colors.TEXT_PRIMARY, borderwidth=0)
    style.configure("Treeview.Heading", background=Colors.BG_PANEL, foreground=Colors.TEXT_PRIMARY, font=("Segoe UI", 10, "bold"))
    style.map("Treeview", background=[('selected', Colors.ACCENT)])
    
    # Notebook
    style.configure("TNotebook", background=Colors.BG_MAIN, borderwidth=0)
    style.configure("TNotebook.Tab", background=Colors.BG_PANEL, foreground=Colors.TEXT_PRIMARY, padding=[10, 5])
    style.map("TNotebook.Tab", background=[("selected", Colors.BG_SECONDARY)])
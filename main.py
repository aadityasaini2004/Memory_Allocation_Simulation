import sys

def main():
    try:
        import tkinter
    except ImportError:
        print("Error: Tkinter is not available in this Python environment.")
        print("Please install python3-tk or the equivalent package for your OS.")
        sys.exit(1)
        
    from gui.app import MemorySimulatorApp
    
    app = MemorySimulatorApp()
    app.mainloop()

if __name__ == '__main__':
    main()
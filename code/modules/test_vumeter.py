import tkinter as tk
from vumeter_real import RealVUMeter

root = tk.Tk()
root.geometry("300x150")
vumeter = RealVUMeter(root)

def on_close():
    vumeter.stop()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
 
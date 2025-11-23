import tkinter as tk
from player import PlaylistPlayer
from tkinterdnd2 import DND_FILES, TkinterDnD
import mutagen
import PIL
import PIL.Image
import PIL.ImageTk

import sys, os
if hasattr(sys, "_MEIPASS"):
    for root, dirs, files in os.walk(sys._MEIPASS):
        print(root, files)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    
    
    app = PlaylistPlayer(root)
    print("Entrando en loop de Tkinter")
    root.mainloop() 

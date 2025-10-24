import tkinter as tk
from player import PlaylistPlayer
from tkinterdnd2 import DND_FILES, TkinterDnD



if __name__ == "__main__":
    root = TkinterDnD.Tk()
    
    app = PlaylistPlayer(root)
    root.mainloop() 

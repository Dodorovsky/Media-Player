
from player import PlaylistPlayer
from tkinterdnd2 import DND_FILES, TkinterDnD


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    
    
    app = PlaylistPlayer(root)
    print("Entrando en loop de Tkinter")
    root.mainloop()

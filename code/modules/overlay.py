# 🛰️ overlay.py — Deploys the floating HUD in fullscreen mode

import tkinter as tk

class FloatingOverlay:
    def __init__(self, root, play_callback, pause_callback, stop_callback):
        self.root = root
        self.overlay_window = None
        self.overlay_visible = False
        self.play_callback = play_callback
        self.pause_callback = pause_callback
        self.stop_callback = stop_callback

    def create_overlay(self):
        if not self.overlay_window:
            self.overlay_window = tk.Toplevel(self.root)
            self.overlay_window.overrideredirect(True)
            self.overlay_window.attributes("-topmost", True)
            self.overlay_window.attributes("-alpha", 0.9)
            self.overlay_window.configure(bg="#222222")

            # Controles flotantes
            play_btn = tk.Button(self.overlay_window, text="▶", command=self.play_callback, bg="#222222", fg="white", bd=0)
            pause_btn = tk.Button(self.overlay_window, text="⏸", command=self.pause_callback, bg="#222222", fg="white", bd=0)
            stop_btn = tk.Button(self.overlay_window, text="⏹", command=self.stop_callback, bg="#222222", fg="white", bd=0)

            play_btn.pack(side="left", padx=10)
            pause_btn.pack(side="left", padx=10)
            stop_btn.pack(side="left", padx=10)
            
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.overlay_window.geometry(f"300x40+{int((screen_width-300)/2)}+{screen_height-50}")
        self.overlay_window.deiconify()
        self.overlay_visible = True

    def show_overlay(self):
        if self.overlay_window:
            self.overlay_window.deiconify()
            self.overlay_window.lift()
            self.overlay_visible = True

            if self.overlay_hide_timer:
                self.root.after_cancel(self.overlay_hide_timer)
            self.overlay_hide_timer = self.root.after(3000, self.hide_overlay)



    def hide_overlay(self):
        if self.overlay_window:
            self.overlay_window.withdraw()
            #self.overlay_visible = False
            
'''    def destroy_overlay(self):
        if self.overlay_window:
            self.overlay_window.destroy()
            self.overlay_window = None
            self.overlay_visible = False
            self.root.unbind("<Motion>")
        self.fullscreen = False
        self.mouse_tracker_active = False'''


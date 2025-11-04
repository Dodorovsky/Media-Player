import tkinter as tk

class FloatingOverlay:
    def __init__(self, master, play_callback, pause_callback, stop_callback, exit_fullscreen_callback ):
        self.master = master
        self.play_callback = play_callback
        self.pause_callback = pause_callback
        self.stop_callback = stop_callback
        self.exit_fullscreen_callback = exit_fullscreen_callback
        self.overlay_window = None
        self.overlay_visible = False
        self.overlay_hide_timer = None
        self.last_mouse_position = None
        self.mouse_tracker_active = False

    def create_overlay(self):
        if self.overlay_window:
            return

        self.overlay_window = tk.Toplevel(self.master)
        self.overlay_window.overrideredirect(True)
        self.overlay_window.attributes("-topmost", True)
        self.overlay_window.attributes("-alpha", 0.9)
        self.overlay_window.configure(bg="#222222")

        play_btn = tk.Button(self.overlay_window, text="▶", command=self.play_callback, bg="#222222", fg="white", bd=0)
        pause_btn = tk.Button(self.overlay_window, text="⏸", command=self.pause_callback, bg="#222222", fg="white", bd=0)
        stop_btn = tk.Button(self.overlay_window, text="⏹", command=self.stop_callback, bg="#222222", fg="white", bd=0)

        play_btn.pack(side="left", padx=10)
        pause_btn.pack(side="left", padx=10)
        stop_btn.pack(side="left", padx=10)
        
        exit_btn = tk.Button(
    self.overlay_window,
    text="⬅ Exit Fullscreen",
    command=self.exit_fullscreen_callback,
    bg="#222222",
    fg="white",
    bd=0
)
        exit_btn.pack(side="left", padx=10)

        self.position_overlay()
        self.mouse_tracker_active = True
        self.track_mouse()

    def position_overlay(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.overlay_window.geometry(f"300x40+{int((screen_width-300)/2)}+{screen_height-50}")

    def show_overlay(self):
        if self.overlay_window:
            self.overlay_window.deiconify()
            self.overlay_window.lift()
            self.overlay_visible = True
            self.reset_hide_timer()

    def hide_overlay(self):
        if self.overlay_window:
            self.overlay_window.withdraw()
            self.overlay_visible = False

    def reset_hide_timer(self):
        if self.overlay_hide_timer:
            self.master.after_cancel(self.overlay_hide_timer)
        self.overlay_hide_timer = self.master.after(3000, self.hide_overlay)

    def track_mouse(self):
        if not self.mouse_tracker_active:
            return

        x = self.master.winfo_pointerx()
        y = self.master.winfo_pointery()
        current_position = (x, y)

        if self.last_mouse_position != current_position:
            self.last_mouse_position = current_position
            self.show_overlay()

        self.master.after(300, self.track_mouse)

    def destroy_overlay(self):
        if self.overlay_window:
            self.overlay_window.destroy()
            self.overlay_window = None
            self.overlay_visible = False
            self.mouse_tracker_active = False
 
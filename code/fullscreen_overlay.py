import tkinter as tk

class FullscreenOverlay:
    def __init__(self, parent, play_callback, pause_callback, stop_callback):
        self.parent = parent  # normalmente será video_frame o su contenedor
        self.play_callback = play_callback
        self.pause_callback = pause_callback
        self.stop_callback = stop_callback

        self.overlay_visible = False
        self.hide_timer = None

        self.overlay_frame = tk.Frame(self.parent, bg="#222222", height=40)
        self.overlay_frame.place(relx=0.5, rely=0.95, anchor="s")
        self.overlay_frame.lower()

        self.play_button = tk.Button(self.overlay_frame, text="▶", command=self.play_callback, bg="#222222", fg="white", bd=0)
        self.play_button.grid(side="left", padx=5)

        self.pause_button = tk.Button(self.overlay_frame, text="⏸", command=self.pause_callback, bg="#222222", fg="white", bd=0)
        self.pause_button.grid(side="left", padx=5)

        self.stop_button = tk.Button(self.overlay_frame, text="⏹", command=self.stop_callback, bg="#222222", fg="white", bd=0)
        self.stop_button.grid(side="left", padx=5)

        self.parent.bind("<Motion>", self.on_mouse_move)

    def on_mouse_move(self, event=None):
        if getattr(self, "fullscreen", False):
            self.show_overlay()

    def show_overlay(self):
        if not self.overlay_visible:
            self.overlay_frame.lift()
            self.overlay_visible = True
        if self.hide_overlay_timer:
            self.root.after_cancel(self.hide_overlay_timer)
        self.hide_overlay_timer = self.root.after(3000, self.hide_overlay)

    def hide_overlay(self):
        if self.overlay_frame:
            self.overlay_frame.lower()
            self.overlay_visible = False




'''    def destroy(self):
        self.overlay_frame.destroy()'''

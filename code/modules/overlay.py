import tkinter as tk

class FloatingOverlay:
    def __init__(self, master, play_callback, pause_callback, stop_callback, exit_fullscreen_callback, seek_callback, get_time_callback, get_length_callback ):
        self.master = master
        self.play_callback = play_callback
        self.pause_callback = pause_callback
        self.stop_callback = stop_callback
        self.exit_fullscreen_callback = exit_fullscreen_callback
        self.seek_callback = seek_callback
        self.get_time_callback = get_time_callback
        self.get_length_callback = get_length_callback
        
        self.overlay_window = None
        self.overlay_visible = False
        self.overlay_hide_timer = None
        self.last_mouse_position = None
        self.mouse_tracker_active = False
        self.play_pause_btn = None
        self.is_playing = False  
        self.time_slider = None
        self.slider_update_active = False
        self.ignore_slider_callback = False
        self.slider_being_dragged = False



    def create_overlay(self):
        if self.overlay_window:
            return

        self.overlay_window = tk.Toplevel(self.master)
        self.overlay_window.withdraw()
        self.overlay_window.overrideredirect(True)
        self.overlay_window.attributes("-topmost", True)
        self.overlay_window.attributes("-alpha", 0.9)
        self.overlay_window.configure(bg="#222222")
        


        self.play_pause_btn = tk.Button(
            self.overlay_window,
            text="⏸",
            command=self.toggle_play_pause,
            bg="#222222",
            fg="white",
            bd=0
        )
        self.play_pause_btn.pack(side="left", padx=10)

        stop_btn = tk.Button(self.overlay_window, text="⏹", command=self.stop_callback, bg="#222222", fg="white", bd=0)

        #play_btn.pack(side="left", padx=10)
        #pause_btn.pack(side="left", padx=10)
        stop_btn.pack(side="left", padx=10)
        
        self.time_label = tk.Label(
            self.overlay_window,
            text="00:00 / 00:00",
            bg="#222222",
            fg="white",
            font=("Arial", 10)
        )
        self.time_label.pack(side="left", padx=10)
        
        exit_btn = tk.Button(
    self.overlay_window,
    text="⬅ Exit Fullscreen",
    command=self.exit_fullscreen_callback,
    bg="#222222",
    fg="white",
    bd=0
)
        exit_btn.pack(side="left", padx=10)
        
        self.time_slider = tk.Scale(
            self.overlay_window,
            from_=0,
            to=100,
            orient="horizontal",
            length=450,
            showvalue=False,
            bg="#5A3A3A",
            fg="yellow",
            troughcolor="#444444",
            highlightthickness=0,
            bd=0,
            sliderrelief="flat",
            command=self.on_slider_move
        )
        self.time_slider.pack(side="left", padx=10, fill="x", expand=True)
        self.time_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.time_slider.bind("<ButtonRelease-1>", self.on_slider_release)


        self.position_overlay()
        self.mouse_tracker_active = False
       
    def toggle_play_pause(self):
        if self.is_playing:
            self.pause_callback()
            self.play_pause_btn.config(text="▶")
            self.is_playing = False
        else:
            self.play_callback()
            self.play_pause_btn.config(text="⏸")
            self.is_playing = True

    def position_overlay(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.overlay_window.geometry(f"600x40+{int((screen_width-300)/2)}+{screen_height-50}")

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
            
    def on_slider_move(self, value):
        if self.ignore_slider_callback or not self.slider_being_dragged:
            return

        try:
            percent = float(value)
            total_length = self.get_length_callback()
            new_time = int((percent / 100) * total_length)
            self.seek_callback(new_time)
        except Exception as e:
            print("Error in slider move:", e)
 
    def start_slider_update(self, get_time_callback, get_length_callback):
        self.get_time_callback = get_time_callback
        self.get_length_callback = get_length_callback
        self.slider_update_active = True
        self.update_slider_position()
        
    def update_slider_position(self):
        if not self.slider_update_active or not self.time_slider:
            return

        current_time = self.get_time_callback()
        total_length = self.get_length_callback()

        if total_length > 0:
            percent = int((current_time / total_length) * 100)

            self.ignore_slider_callback = True  # ⛔ Bloqueamos el callback
            self.time_slider.set(percent)
            self.ignore_slider_callback = False  # ✅ Lo reactivamos

            current_str = self.format_time(current_time)
            total_str = self.format_time(total_length)
            self.time_label.config(text=f"{current_str} / {total_str}")

        self.overlay_window.after(1000, self.update_slider_position)
     
    def resume_slider_update(self):
        self.slider_update_active = True
        self.update_slider_position()  # ✅ Forzamos una actualización inmediata

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02}:{secs:02}"

    def start_mouse_tracking(self):
        if not self.mouse_tracker_active:
            self.mouse_tracker_active = True
            self.track_mouse()

    def stop_mouse_tracking(self):
        self.mouse_tracker_active = False

    def on_slider_press(self, event):
        self.slider_being_dragged = True
        self.slider_update_active = False  # Pausamos la actualización automática

    def on_slider_release(self, event):
        self.slider_being_dragged = False
        self.overlay_window.after(1500, self.resume_slider_update)


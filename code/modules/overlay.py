import tkinter as tk

class FloatingOverlay:
    def __init__(self, master, play_callback, pause_callback, stop_callback, exit_fullscreen_callback, seek_callback, get_time_callback, get_length_callback ):
        # Initialize floating overlay with callbacks for playback, fullscreen, and seeking
        # Store state variables for overlay visibility, mouse tracking, and slider interaction
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
        # Create overlay window with playback controls, time label, exit button, and time slider
        # Configure window as transparent, topmost, and frameless
        self.overlay_window = tk.Toplevel(self.master)
        self.overlay_window.withdraw()
        self.overlay_window.overrideredirect(True)
        self.overlay_window.attributes("-topmost", True)
        self.overlay_window.attributes("-alpha", 0.9)
        self.overlay_window.configure(bg="#222222")
        
        self.play_pause_btn = tk.Button(
            self.overlay_window,
            text="⏸", font=("Terminal", 12),
            command=self.toggle_play_pause,
            bg="#222222",
            fg="white",
            bd=0
        )
        self.play_pause_btn.place(relx=0.44, rely=0.3, anchor="center")

        stop_btn = tk.Button(self.overlay_window, text="⏹", font=("Terminal", 12), command=self.stop_callback, bg="#222222", fg="white", bd=0)
        stop_btn.place(relx=0.46, rely=0.3, anchor="center")
        
        self.time_label = tk.Label(
            self.overlay_window,
            text="00:00 / 00:00",
            bg="#222222",
            fg="green",
            font=("Terminal", 10)
        )
        self.time_label.place(relx=0.50, rely=0.3, anchor="center")
        
        exit_btn = tk.Button(
    self.overlay_window,
    text="⬅ Exit Fullscreen",
    command=self.exit_fullscreen_callback,
    bg="#5F5C5C",
    fg="white",
    bd=0
)
        exit_btn.place(relx=0.56, rely=0.3, anchor="center")
        
        self.time_slider = tk.Scale(
            self.overlay_window,
            from_=0,
            to=100,
            orient="horizontal",
            length=600,
            showvalue=False,
            bg="#F1E724",
            fg="green",
            troughcolor="#807B7B",
            highlightthickness=0,
            bd=0,
            sliderrelief="flat",
            command=self.on_slider_move
        )

        self.time_slider.place(relx=0, rely=1, anchor="sw", relwidth=1.0, y=-20)
        self.time_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.time_slider.bind("<ButtonRelease-1>", self.on_slider_release)


        self.position_overlay()
        self.mouse_tracker_active = False
       
    def toggle_play_pause(self):
        # Toggle between play and pause states, updating button icon accordingly
        if self.is_playing:
            self.pause_callback()
            self.play_pause_btn.config(text="▶")
            self.is_playing = False
        else:
            self.play_callback()
            self.play_pause_btn.config(text="⏸")
            self.is_playing = True

    def position_overlay(self):
        # Position overlay at the bottom of the screen with fixed height
        overlay_height = 100
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.overlay_window.geometry(f"{screen_width}x{overlay_height}+0+{screen_height - overlay_height}")

    def show_overlay(self):
        # Show overlay window and reset auto-hide timer
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
        # Reset auto-hide timer (overlay hides after 1.5 seconds of inactivity)
        if self.overlay_hide_timer:
            self.master.after_cancel(self.overlay_hide_timer)
        self.overlay_hide_timer = self.master.after(1500, self.hide_overlay)

    def track_mouse(self):
        if not self.mouse_tracker_active:
            return
        
        # Track mouse movement; show overlay when position changes
        x = self.master.winfo_pointerx()
        y = self.master.winfo_pointery()
        current_position = (x, y)

        if self.last_mouse_position != current_position:
            self.last_mouse_position = current_position
            self.show_overlay()

        self.master.after(300, self.track_mouse)

    def destroy_overlay(self):
        # Destroy overlay window and reset state variables
        if self.overlay_window:
            self.overlay_window.destroy()
            self.overlay_window = None
            self.overlay_visible = False
            self.mouse_tracker_active = False
            
    def on_slider_move(self, value):
        # Update time label while dragging slider (preview new position)
        if self.ignore_slider_callback or not self.slider_being_dragged:
            return

        self.time_label.configure(fg="#C2A53B")    
        try:
            percent = float(value)
            total_length = self.get_length_callback()
            new_time = int((percent / 100) * total_length)
            current_str = self.format_time(new_time)
            total_str = self.format_time(total_length)
            self.time_label.config(text=f"{current_str} / {total_str}")
            
        except Exception as e:
            print("Error in slider move:", e)

    def start_slider_update(self, get_time_callback, get_length_callback):
        # Start automatic slider updates based on playback time
        self.get_time_callback = get_time_callback
        self.get_length_callback = get_length_callback
        self.slider_update_active = True
        self.update_slider_position()
        
    def update_slider_position(self):
        if not self.slider_update_active or not self.time_slider:
            return
        # Update slider position and time label every second
        current_time = self.get_time_callback()
        total_length = self.get_length_callback()

        if total_length > 0:
            percent = int((current_time / total_length) * 100)
            self.ignore_slider_callback = True 
            self.time_slider.set(percent)
            self.ignore_slider_callback = False

            current_str = self.format_time(current_time)
            total_str = self.format_time(total_length)
            self.time_label.config(text=f"{current_str} / {total_str}")

        self.overlay_window.after(1000, self.update_slider_position)
     
    def resume_slider_update(self):
        #Resume slider updates after manual drag
        self.slider_update_active = True
        self.update_slider_position() 

    def format_time(self, seconds):
        # Format seconds into mm:ss string
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02}:{secs:02}"

    def start_mouse_tracking(self):
        # Enable mouse tracking loop
        if not self.mouse_tracker_active:
            self.mouse_tracker_active = True
            self.track_mouse()

    def stop_mouse_tracking(self):
        # Disable mouse tracking loop
        self.mouse_tracker_active = False

    def on_slider_press(self, event):
        # Mark slider as being dragged and pause automatic updates
        self.slider_being_dragged = True
        self.slider_update_active = False 

    def on_slider_release(self, event):
        # Seek to new position after drag and resume updates
        self.slider_being_dragged = False
        percent = self.time_slider.get()
        total_length = self.get_length_callback()
        new_time = int((percent / 100) * total_length)
        self.seek_callback(new_time)
        self.time_label.config(fg="green")

        self.overlay_window.after(1500, self.resume_slider_update)



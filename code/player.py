from modules.utils import format_time
from modules.vumeter_real import RealVUMeter

from modules.overlay import FloatingOverlay
from ui2 import setup_ui
import tkinter as tk
from tkinter import filedialog, messagebox 
import tkinter.ttk as ttk
import vlc
import os
import random

import platform 

class PlaylistPlayer:
    def __init__(self, root):
        self.root = root
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        self.playlist = []
        self.current_index = None
        self.duration = 0
        self.updating_slider = False
        
        setup_ui(self)
        self.bind_events()
        self.update_time()
        self.loop_enabled = False
        self.shuffle_enabled = False      
        self.overlay_window = None
        self.overlay_visible = False
        self.overlay_hide_timer = None
        self.last_mouse_position = None
        self.mouse_tracker_active = False
        self.pantlla_completa = False
        
        self.overlay = FloatingOverlay(
    master=self.root,
    play_callback=self.play_from_selection,
    pause_callback=self.pause,
    exit_fullscreen_callback = self.exit_fullscreen_video,
    stop_callback=self.stop
    
)
        
       
    def bind_events(self):
        self.listbox.bind("<Double-Button-1>", self.on_double_click)
        self.time_slider.bind("<ButtonRelease-1>", self.seek_on_release)

    def load_files(self):
        # 📂 Opens file dialog to select multiple media files
        files = filedialog.askopenfilenames()

        if files:
            self.playlist = list(files)
            # 🧹 Clears the current listbox display
            self.listbox.delete(0, tk.END)

            for f in self.playlist:
                self.listbox.insert(tk.END, os.path.basename(f))
                self.current_file_is_audio = f.lower().endswith((".mp3", ".wav", ".flac"))
            self.pantlla_completa =False
            # 🔊 Auto-launch: selects and plays the first track
            self.current_index = 0
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.play_from_selection()
                    
    def play_from_selection(self):
        if self.current_index is None:
            return
        filepath = self.playlist[self.current_index]

        # Create the Media and assign it to the Player
        media = self.vlc_instance.media_new(filepath)
        self.player.set_media(media)

        # 📼 Detect if it is video
        if filepath.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            self.listbox.grid_remove()
            self.video_frame.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nsew")
        
            self.root.update_idletasks()
            self.embed_video()     
        else:
            self.video_frame.grid_remove()
            self.listbox.grid(row=1, column=0, columnspan=2)#, columnspan=2
            
        if self.pantlla_completa:
            self.video_frame.grid(row=0, column=0, sticky="nsew")
            self.top_frame.grid_rowconfigure(0, weight=1)
            self.top_frame.grid_columnconfigure(0, weight=1)
            self.video_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
                        
        self.player.play()

        # ⏱️ Update duration and time after playing
        self.root.after(500, self.set_duration)
        self.update_time()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop() # ⏹️ Stop playback and reset UI
        self.updating_slider = True
        self.time_slider.set(0)
        self.current_time_label.config(text="00:00")
        self.updating_slider = False
                    
    def play_previous(self):
        if self.current_index is not None and self.current_index > 0:
            self.current_index -= 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.listbox.activate(self.current_index)
            self.play_from_selection()

    def play_next(self):
        if not self.playlist:
            return

        if self.shuffle_enabled:
            next_index = random.randint(0, len(self.playlist) - 1)
            # 🎶 Avoid repeating the same song
            while next_index == self.current_index and len(self.playlist) > 1:
                next_index = random.randint(0, len(self.playlist) - 1)
            self.current_index = next_index
        else:
            if self.current_index is not None and self.current_index < len(self.playlist) - 1:
                self.current_index += 1
            else:
                return  # End of list

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.current_index)
        self.listbox.activate(self.current_index)
        self.play_from_selection()
      
    def set_volume(self, val):
        vol = int(float(val))
        self.player.audio_set_volume(vol)
        self.volume_label.config(text=f"{vol}")

    def set_duration(self):
        # Wait until VLC loads the media to get its duration
        length = self.player.get_length()
        if length > 0:
            self.duration = length
            self.time_slider.config(to=length)
            self.total_time_label.config(text=f"{format_time(length)}")
        else:
            # Try again shortly if duration is not yet available
            self.root.after(500, self.set_duration)

    def seek_on_release(self, event):
        val = self.time_slider.get()
        self.player.set_time(int(val))
            
    def update_time(self):
        current_time = self.player.get_time()
        if self.player.is_playing():
            if current_time >= 0 and current_time != self.time_slider.get():
                self.updating_slider = True
                self.time_slider.set(current_time)
                self.current_time_label.config(text=format_time(current_time))
                self.updating_slider = False
        else:
            # If it is not playing and the current time is near the end
            if self.duration > 0 and current_time >= self.duration - 1000:
                if self.loop_enabled:
                    self.play_from_selection()
                else:
                    self.play_next()

        self.root.after(1000, self.update_time)
          
    def on_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.current_index = selection[0]
            self.play_from_selection()
            
    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled
        state =  "#7FF530" if self.loop_enabled else "#C2DDAC"
        self.loop_button.config(bg=f"{state}")

    def toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled
        color = "#7FF530" if self.shuffle_enabled else "#C2DDAC"
        self.shuffle_button.config(bg=color)

    def on_drop(self, event):
        # 📂 Extract list of dropped files from the drag event
        files = self.root.tk.splitlist(event.data)
        
        SUPPORTED_FORMATS = (
    '.mp3', '.wav', '.flac',  # 🎶 Audio
    '.mp4', '.avi', '.mkv', '.mov', '.webm'  # 🎥 Video
)

        for f in files:
            if f.lower().endswith(SUPPORTED_FORMATS):
                self.playlist.append(f)
                self.listbox.insert(tk.END, os.path.basename(f))
            else:             
                self.video_frame.grid_remove()
                self.listbox.grid(row=1, column=0) 
                
                # 🔁 Attempt to play current selection (fallback behavior)
                self.play_from_selection()

        # 🔊 Auto-play last added file if nothing is currently playing
        if self.current_index is None and self.playlist:
            self.current_index = len(self.playlist) - 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.listbox.activate(self.current_index)
            self.play_from_selection()

    def embed_video(self):
        # 📺 Embed video stream into the UI frame based on OS
        video_id = self.video_frame.winfo_id()
        system = platform.system()

        if system == "Windows":
            self.player.set_hwnd(video_id)
        elif system == "Linux":
            self.player.set_xwindow(video_id)
        elif system == "Darwin":  # macOS
            self.player.set_nsobject(video_id)
        else:
            print("Unsupported system to embed video.")

    def toggle_fullscreen(self):
        self.fullscreen = not getattr(self, "fullscreen", False)
        self.root.attributes("-fullscreen", self.fullscreen)

        if self.fullscreen:
            # Hide elements
            self.listbox.grid_remove()
            self.control_frame.grid_remove()
            self.slider.grid_remove()
        else:
            # Restore elements
            self.listbox.grid()
            self.control_frame.grid()
            self.slider.grid()

    def enter_fullscreen_video(self):
        if self.current_file_is_audio:
            messagebox.showinfo("Full screen mode", "Full screen mode is disabled for audio files")
            return  # Lock full screen if it is audio

        self.root.attributes("-fullscreen", True)
        self.mouse_tracker_active = True
        self.track_mouse_movement()
        self.pantlla_completa = True
        
        # Hide all elements except the video
        self.listbox.grid_remove()  
        self.total_time_label.grid_remove()
        self.current_time_label.grid_remove()      
        self.central_frame.grid_remove()  
        self.right_frame.grid_remove()
        self.left_frame.grid_remove()  
        self.time_slider.grid_remove()            
        self.top_frame.grid_rowconfigure(1, minsize=0, weight=0) 
        self.video_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")  # ocupar toda la ventana
        # Expand the video_frame
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        
        # Create floating overlay window
        self.overlay.create_overlay()

        # Detect global movement
        self.track_mouse_movement()

        self.show_overlay()

    def exit_fullscreen_video(self):
        self.root.attributes("-fullscreen", False)

        # Restore elements
        self.main_frame.grid_rowconfigure(0, weight=1)  # vídeo
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)     
        self.listbox.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nsew")
        self.video_frame.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nsew")   
        self.time_slider.grid(row=2, column=0, padx=20, sticky="nsew")
        self.current_time_label.grid(row=3, column=0, padx=(0, 470))
        self.total_time_label.grid(row=3, column=0, padx=(470, 0))

        self.right_frame.grid(row=2, column=2, sticky="n")
        self.left_frame.grid(row=2, column=0, sticky="n")
        self.central_frame.grid(row=2, column=1, sticky="n")
        
        if self.overlay_window:
            self.overlay.destroy_overlay()
            self.overlay_window = None
            self.overlay_visible = False
            self.root.unbind("<Motion>")
        self.fullscreen = False
        self.mouse_tracker_active = False
     
    def on_mouse_move(self, event=None):
        if getattr(self, "fullscreen", False):
            self.show_overlay()

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
            
    def track_mouse_movement(self):
        if not self.mouse_tracker_active:
            return

        # Get relative mouse position within root
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        current_position = (x, y)

        if self.last_mouse_position != current_position:
            self.last_mouse_position = current_position
            self.show_overlay()

        self.root.after(300, self.track_mouse_movement)




    





        

        





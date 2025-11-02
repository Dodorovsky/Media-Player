from modules.utils import format_time
#from modules.vumeter_real import RealVUMeter
#from modules.vu_meter_experiment import VUMeterExperimental
from modules.vu_meter_experiment import VUColumn

from modules.overlay import FloatingOverlay
from ui import setup_ui
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
        self.pause = False
        self.stop = False
        self.play = False
        
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
        self.stop_button.config(image=self.stop_off)

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
        self.play_button.config(image=self.play_on)
        # Create the Media and assign it to the Player
        media = self.vlc_instance.media_new(filepath)
        self.player.set_media(media)
        

        # 📼 Detect if it is video
        if filepath.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            self.listbox.grid_remove()
            self.video_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
            
            self.root.update_idletasks()
            self.embed_video()     
        else:
            self.video_frame.grid_remove()
            self.listbox.grid(row=1, column=0, padx=0, pady=0) 
            self.power_on_label.grid(row=0, column=0, padx=(250,0), pady=(5,0))
            self.hal_label.grid(row=0, column=1,pady=(5,5))
            self.stop_button.config(image=self.stop_off )
            self.pause_button.config(image=self.pause_off)
            self.left_vu_label.config(fg="#CAFFFE")
            self.right_vu_label.config(fg="#CAFFFE")
            self.current_time_label.config(fg="#CAFFFE")
            self.total_time_label.config(fg="#CAFFFE")
            self.volume_label.config(fg="#CAFFFE")
            self.play = True
            self.stop = False

            
        if self.pantlla_completa:
            self.video_frame.grid(row=0, column=0, sticky="nsew")
            self.video_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
                        
        self.player.play()

        # ⏱️ Update duration and time after playing
        self.root.after(500, self.set_duration)
        self.update_time()

    def pause(self):

        self.player.pause()
        
        if self.stop:
            self.pause_button.config(image=self.pause_off)
            self.left_vu_label.config(fg="#E9E4B2")
            self.right_vu_label.config(fg="#E9E4B2")
            self.volume_label.config(fg="#E9E4B2")

        elif not self.pause and  self.play:
            self.play_button.config(image=self.play_off)
            self.pause_button.config(image=self.pause_on)
            self.left_vu_label.config(fg="#E9E4B2")
            self.right_vu_label.config(fg="#E9E4B2")
            self.current_time_label.config(fg="#E9E4B2")
            self.total_time_label.config(fg="#E9E4B2")
            self.volume_label.config(fg="#E9E4B2")
            #self.stop_button.config(image=self.stop_btn_img )
            self.pause = True
            self.play = False
                  
        elif self.pause and not self.play:
            self.play_button.config(image=self.play_on)
            self.pause_button.config(image=self.pause_off)
            self.left_vu_label.config(fg="#CAFFFE")
            self.right_vu_label.config(fg="#CAFFFE")
            self.current_time_label.config(fg="#CAFFFE")
            self.total_time_label.config(fg="#CAFFFE")
            self.volume_label.config(fg="#CAFFFE")
            self.pause = False
            self.play = True
            
        elif self.pause and self.play:
            self.pause_button.config(image=self.pause_on)
            self.play_button.config(image=self.play_off)
            self.left_vu_label.config(fg="#E9E4B2")
            self.right_vu_label.config(fg="#E9E4B2")
            self.current_time_label.config(fg="#E9E4B2")
            self.total_time_label.config(fg="#E9E4B2")
            self.volume_label.config(fg="#E9E4B2")
            self.pause = False
            self.play = False
        elif not self.pause and not self.play:
            self.play_button.config(image=self.play_on)
            self.pause_button.config(image=self.pause_off)
            self.left_vu_label.config(fg="#CAFFFE")
            self.right_vu_label.config(fg="#CAFFFE")
            self.current_time_label.config(fg="#CAFFFE")
            self.total_time_label.config(fg="#CAFFFE")
            self.volume_label.config(fg="#CAFFFE")
            self.play = True
        else:
            pass
           
    def stop(self):
        self.player.stop() # ⏹️ Stop playback and reset UI
        self.updating_slider = True
        self.time_slider.set(0)
        self.current_time_label.config(text="00:00")
        self.updating_slider = False
        self.play_button.config(image=self.play_off)
        self.stop_button.config(image=self.stop_on)
        self.pause_button.config(image=self.pause_off)
        self.left_vu_label.config(fg="#E9E4B2")
        self.right_vu_label.config(fg="#E9E4B2")
        self.current_time_label.config(fg="#E9E4B2")
        self.total_time_label.config(fg="#E9E4B2")
        self.volume_label.config(fg="#E9E4B2")
        self.stop = True
        self.play = False
                    
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
        self.loop_button.config(bg="f{state}")

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
            return
        self.root.update_idletasks()
        self.root.attributes("-fullscreen", True)
        self.mouse_tracker_active = True
        self.track_mouse_movement()
        self.pantlla_completa = True

        # Ocultar todos los elementos excepto el video
        self.black_frame.grid_remove()
        self.controls_frame.grid_remove()
        self.central_frame.grid_remove()
        self.right_frame.grid_remove()
        self.left_frame.grid_remove()
        self.vu_frame_left.grid_remove()
        self.vu_frame_right.grid_remove()
        
        self.listbox.grid_remove()
        self.time_slider.grid_remove()
        self.current_time_label.grid_remove()
        self.total_time_label.grid_remove()
        
        self.main_frame.grid_rowconfigure(1, weight=0, minsize=0)
        self.main_frame.grid_rowconfigure(2, weight=0, minsize=0)

        self.top_frame.grid_rowconfigure(0, minsize=0, weight=0) 
        self.top_frame.grid_rowconfigure(2, minsize=0, weight=0)
        self.top_frame.grid_rowconfigure(3, minsize=0, weight=0)  
        self.video_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        
        #self.main_frame.grid_rowconfigure(0, weight=1)
        #self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.top_frame.grid_rowconfigure(1, weight=1)
        
        self.top_frame.grid_columnconfigure(0, weight=1)

 
        # Create floating overlay window
        self.overlay.create_overlay()

        # Detect global movement
        self.track_mouse_movement()

        self.show_overlay()

    def exit_fullscreen_video(self):
        self.root.attributes("-fullscreen", False)

        # Restore elements
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=1)

        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)   
        
        self.black_frame.grid(sticky="nsew")
        self.hal_label.grid(row=0, column=1,pady=(5,0))
        self.power_on_label.grid(row=0, column=0, padx=(250,0), pady=(5,0))
        self.video_frame.grid(row=1, column=0, padx=0, pady=(0), sticky="nsew")
        self.time_slider.grid(row=2, column=0, padx=0, sticky="nsew")
        self.current_time_label.grid(row=3, column=0, padx=(0, 540))
        self.total_time_label.grid(row=3, column=0, padx=(540, 0))
    
        self.controls_frame.grid(row=0, column=1, padx=(30, 0), pady=(5,0))
        self.vu_frame_left.grid(row=2, column=0, padx=0, sticky="w")
        self.vu_frame_right.grid(row=2, column=4, sticky="e")
        self.right_frame.grid(row=2, column=3, sticky="n")
        self.left_frame.grid(row=2, column=1, sticky="n")
        self.central_frame.grid(row=2, column=2, sticky="n")

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


    def breathe_hal(self, index=0, direction=1):
            self.hal_label.configure(image=self.hal_frames[index])
            next_index = index + direction
            if next_index == len(self.hal_frames) or next_index < 0:
                    direction *= -1
                    next_index = index + direction
            self.root.after(750, lambda: self.breathe_hal(next_index, direction))




        

        





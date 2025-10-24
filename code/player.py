from utils import format_time
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import vlc
import os
from ui2 import setup_ui
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
          
        
        
    def bind_events(self):
        self.listbox.bind("<Double-Button-1>", self.on_double_click)
        self.time_slider.bind("<ButtonRelease-1>", self.seek_on_release)

    def load_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.playlist = list(files)
            self.listbox.delete(0, tk.END)
            for f in self.playlist:
                self.listbox.insert(tk.END, os.path.basename(f))


                

            # Reproducir automáticamente el primer track
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

        # Detect if it is video
        if filepath.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            #self.toggle_fullscreen()
            self.listbox.grid_remove()
            self.video_frame.grid(row=1, column=0, columnspan=2)     
            self.root.update_idletasks()
            self.embed_video()     
        else:
            self.video_frame.grid_remove()
            self.listbox.grid(row=1, column=0, columnspan=2)
            
        self.player.play()

        # Update duration and time after playing
        self.root.after(500, self.set_duration)
        self.update_time()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
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
            # Evitar repetir la misma canción
            while next_index == self.current_index and len(self.playlist) > 1:
                next_index = random.randint(0, len(self.playlist) - 1)
            self.current_index = next_index
        else:
            if self.current_index is not None and self.current_index < len(self.playlist) - 1:
                self.current_index += 1
            else:
                return  # Fin de la lista

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
            self.total_time_label.config(text=f"{self.format_time(length)}")
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
                self.current_time_label.config(text=self.format_time(current_time))
                self.updating_slider = False
        else:
            # Si no está reproduciendo y el tiempo actual está cerca del final
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

    def format_time(self, ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"
            
    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled
        estado =  "#7FF530" if self.loop_enabled else "#C2DDAC"
        self.loop_button.config(bg=f"{estado}")

    def toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled
        color = "#7FF530" if self.shuffle_enabled else "#C2DDAC"
        self.shuffle_button.config(bg=color)

    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
            
        for f in files:
            if f.lower().endswith(('.mp3', '.wav', '.flac', '.mp4', '.avi', '.mkv')):
                self.playlist.append(f)
                self.listbox.insert(tk.END, os.path.basename(f))
            else:
                self.video_frame.grid_remove()
                self.listbox.grid(row=1, column=0, columnspan=2)

                self.play_from_selection()



        # Automatically play the first one if nothing is playing
        if self.current_index is None and self.playlist:
            self.current_index = len(self.playlist) - 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.listbox.activate(self.current_index)
            self.play_from_selection()

    def embed_video(self):
        
        #self.root.update()
        
        video_id = self.video_frame.winfo_id()
        system = platform.system()

        if system == "Windows":
            self.player.set_hwnd(video_id)
        elif system == "Linux":
            self.player.set_xwindow(video_id)
        elif system == "Darwin":  # macOS
            self.player.set_nsobject(video_id)
        else:
            print("Sistema no compatible para incrustar vídeo.")

    def toggle_fullscreen(self):
        self.fullscreen = not getattr(self, "fullscreen", False)
        self.root.attributes("-fullscreen", self.fullscreen)

        if self.fullscreen:
            # Ocultar otros elementos
            self.listbox.grid_remove()
            self.control_frame.grid_remove()
            self.slider.grid_remove()
        else:
            # Restaurar elementos
            self.listbox.grid()
            self.control_frame.grid()
            self.slider.grid()

    def enter_fullscreen_video(self):
        self.root.attributes("-fullscreen", True)

        # Ocultar todos los elementos excepto el vídeo
        self.listbox.grid_remove()
        
        self.total_time_label.grid_remove()
        self.current_time_label.grid_remove()
        
        self.central_frame.grid_remove()  # si tenés un frame con botones
        self.right_frame.grid_remove()  # si tenés un frame con botones
        self.left_frame.grid_remove()  # si tenés un frame con botones
        self.time_slider.grid_remove()         # si tenés un slider de tiempo
        
        self.top_frame.grid_rowconfigure(1, minsize=0, weight=0)
        
        self.video_frame.grid(row=0, column=0, sticky="nsew")  # ocupar toda la ventana
        

        # Expandir el video_frame

        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)

    def exit_fullscreen_video(self):
        self.root.attributes("-fullscreen", False)

        # Restaurar elementos
  
        self.main_frame.grid_rowconfigure(0, weight=1)  # vídeo
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        
        self.video_frame.grid(row=1, column=0,  padx=20, pady=(20, 0))
        
        self.time_slider.grid(row=2, column=0, padx=20, sticky="nsew")

        
        self.right_frame.grid(row=2, column=2, sticky="n")
        self.left_frame.grid(row=2, column=0, sticky="n")
        self.central_frame.grid(row=2, column=1, sticky="n")
        
        self.current_time_label.grid(row=3, column=0, padx=(0, 630))# side="left", padx=30, pady=(0,54)
        self.total_time_label.grid(row=3, column=0, padx=(630, 0))# side="right", padx=30, pady=(0,54)


        

        







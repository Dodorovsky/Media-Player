from modules.utils import format_time
from mutagen import File
from modules.overlay import FloatingOverlay
from ui import setup_ui
import tkinter as tk
from tkinter import filedialog, messagebox 
import tkinter.ttk as ttk
import vlc
import os
import shutil
import uuid
import tempfile
from pathlib import Path
import random
from pathlib import Path
import platform 

from modules import playlist_manager

class PlaylistPlayer:
    def __init__(self, root):
        # Initialize main window and VLC player instance
        self.root = root
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()
        self.eq = vlc.AudioEqualizer()
        self.root.bind("<space>", self.toggle_play_pause)
        self.root.bind("<h>", self.show_hotkeys)
        self.root.bind("<Left>", self.play_previous)
        self.root.bind("<Right>", self.play_next)
        self.root.bind("<Up>", self.volume_up)
        self.root.bind("<Down>", self.volume_down)
        self.root.bind("<m>", self.toggle_mute)
        # Configure equalizer and initial state
        self.eq.set_preamp(10.0)
        self.playlist = []
        self.current_index = None
        self.duration = 0
        self.updating_slider = False
        # Setup UI and event bindings
        setup_ui(self)
        self.bind_events()
        self.update_time()
        
        # Playback and UI state flags
        self.loop_enabled = False
        self.shuffle_enabled = False      
        self.overlay_window = None
        self.overlay_visible = False
        self.overlay_hide_timer = None
        self.last_mouse_position = None
        self.mouse_tracker_active = False
        self.pantlla_completa = False
        self.pausa = False
        self.stopp = False
        self.playy = False
        self.is_muted = False
        self.last_volume = 50
        self.is_compact = False
        self.eq_t = False
        self.subtitles_path = None
        self.slider_dragging = False
        self.init_eq()
        self.eq_color = "eq_light"
        
        # Floating overlay for playback controls
        self.overlay = FloatingOverlay(
    master=self.root,
    play_callback=self.play,
    pause_callback=self.pause,
    exit_fullscreen_callback = self.exit_fullscreen_video,
    stop_callback=self.stop,
    seek_callback = self.seek_to_time,
        get_time_callback=self.get_current_time,
    get_length_callback=self.get_total_length
    
)
       
    def bind_events(self):
        # Bind UI events for listbox and time slider
        self.listbox.bind("<Double-Button-1>", self.on_double_click)
        self.time_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.time_slider.bind("<ButtonRelease-1>", self.on_slider_release)

    def load_files(self):
        # Open file dialog and load selected files into playlist
        files = filedialog.askopenfilenames()
        self.stop_button.config(image=self.stop_off)
        self.placeholder.place_forget()
        self.logo_listbox.place_forget()
        self.player.stop()
        self.player.release()
        self.player = self.vlc_instance.media_player_new()

        # Reset radio button colors
        for btn in self.radio_buttons.values():
            btn.config(bg="#191818")
        if files:
            self.playlist = list(files)
            self.listbox.delete(0, tk.END)
            for f in self.playlist:
                self.current_file_is_audio = f.lower().endswith((".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma", ".aiff", ".alac"))
                if self.current_file_is_audio:
                    self.video_frame.grid_remove()
                    #self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
                    #self.listbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew") 
                    self.top_frame.configure(bg='#181717')
                    self.load_file_in_listbox(f)                 
                else:
                    # Non-audio files are added directly
                    self.listbox.insert(tk.END, os.path.basename(f))
                    
            # Reset playback state
            self.pantlla_completa =False
            self.current_index = 0
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.play_from_selection()
        self.playlist_button.config(bg="#BC853D")
          
    def play_from_selection(self):
        # Play the file currently selected in the playlist
        if self.current_index is None:
            print("Kein Element in der Playlist ausgewählt.")
            return
        
        filepath = self.playlist[self.current_index]
        media = self.vlc_instance.media_new(filepath)
        
        # Load subtitles if available
        auto_sub = Path(filepath).with_suffix(".srt")
        if self.subtitles_path:
            ruta_sub = Path(self.subtitles_path).as_posix()
            media.add_option(f'sub-file="{ruta_sub}"') 
        self.player.set_media(media)
        self.player.play()
        
        # Configure UI depending on file type (video vs audio)
        if filepath.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            # Video playback UI
            self.listbox.grid_remove()
            self.video_frame.grid(row=1, column=0, sticky="nsew")
            self.black_frame.grid(row=0, pady=0, columnspan=5, sticky="n")
            self.stop_button.config(image=self.stop_off )
            self.play_pause_button.config(image=self.pause_big)
            self.current_time_label.config(fg="#ADADAD")
            self.total_time_label.config(fg="#ADADAD")
            self.mp6_label_left.config(image=self.mp6)
            self.mp6_label_right.config(image=self.mp6)
            self.volume_label.config(fg="#E9E4B2")
            self.style.configure('Custom.Horizontal.TScale', troughcolor="#B1620D")
            self.eq_color = "eq_light_on_image"
            self.playy = True
            self.parar = False
            self.root.update_idletasks()
            self.embed_video()     
            
        else:
            # Audio playback UI
            self.video_frame.grid_remove()
            self.listbox.grid(row=1, column=0, sticky="nsew")
            self.stop_button.config(image=self.stop_off )
            self.play_pause_button.config(image=self.pause_big)
            self.current_time_label.config(fg="#D19595")
            self.total_time_label.config(fg="#D19595")
            self.volume_label.config(fg="#E9E4B2")
            self.mp6_label_left.config(image=self.mp6)
            self.mp6_label_right.config(image=self.mp6)
            self.style.configure('Custom.Horizontal.TScale', troughcolor="#C28409")
            self.is_playing = True
            self.playy = True
            self.parar = False
        
        # Handle fullscreen mode
        if self.pantlla_completa:
            self.video_frame.grid(row=0, column=0, sticky="nsew")
            self.video_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        
        # Apply equalizer if available    
        if hasattr(self, 'eq') and isinstance(self.eq, vlc.AudioEqualizer):
            self.player.set_equalizer(self.eq)
            
        self.player.play()
        if not self.overlay.overlay_window:
            self.overlay.create_overlay()

        self.overlay.is_playing = True
        self.overlay.play_pause_btn.config(text="⏸")  

        self.root.after(500, self.set_duration)
        self.update_time()
        
    def play_pause(self):
        # Toggle between play and pause
        selection = self.listbox.curselection()
        media = self.player.get_media()
        if not selection and not media:
            return
        if self.player.is_playing():
            self.player.pause()  
            
        else:
            state = self.player.get_state()
            self.player.play()
            if state == vlc.State.Paused:
                self.player.play()
           
    def stop(self):
        # Stop playback and reset UI
        self.player.stop() 
        self.style.configure('Custom.Horizontal.TScale', troughcolor="black")
        self.mp6_label_left.config(image=self.mp6_off)
        self.mp6_label_right.config(image=self.mp6_off)
        self.updating_slider = True
        self.time_slider.set(0)
        self.current_time_label.config(text="00:00")
        self.updating_slider = False
        self.play_pause_button.config(image=self.play_off)
        self.stop_button.config(image=self.stop_on)
        
        self.current_time_label.config(fg="#ADADAD")
        self.total_time_label.config(fg="#ADADAD")
        self.volume_label.config(fg="#E9E4B2")
        self.stopp = True
        self.pausa = False
                    
    def play_previous(self, event=None):
        # Play the previous item in the playlist
        if self.current_index is not None and self.current_index > 0:
            self.current_index -= 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.listbox.activate(self.current_index)
            self.play_from_selection()

    def play_next(self, event=None):
        # Play the next item in the playlist (supports shuffle mode)
        if not self.playlist:
            return
        
        if self.shuffle_enabled:
            # Select a random item different from the current one
            next_index = random.randint(0, len(self.playlist) - 1)
            while next_index == self.current_index and len(self.playlist) > 1:
                next_index = random.randint(0, len(self.playlist) - 1)
            self.current_index = next_index
        else:
            # Sequential playback
            if self.current_index is not None and self.current_index < len(self.playlist) - 1:
                self.current_index += 1
            else:
                return  

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.current_index)
        self.listbox.activate(self.current_index)
        self.play_from_selection()
      
    def set_volume(self, val):
        # Set volume based on slider value
        vol = int(float(val))
        self.player.audio_set_volume(vol)
        self.volume_label.config(text=f"{vol}")
        if vol > 1 and self.is_muted:
            # Unmute if volume is raised
            self.volume_label.config(fg="#CAFFFE")
            self.mute_button.config(bg="#3E3838")
            self.volume_label_frame.config(fg="green")
            self.style.configure('TScale', troughcolor="#AC8433")
            self.is_muted = False
        elif vol < 1 and not self.is_muted:
            # Mute if volume is set to zero
            self.mute_button.config(bg="#D21A1A")
            self.style.configure('TScale', troughcolor="#D21A1A")
            self.is_muted = True
               
    def volume_up(self,  event=None):
        # Increase volume by 1 unit
        volume = self.player.audio_get_volume()
        volume += 1
        self.player.audio_set_volume(volume)
        self.volume_label.config(text=f"{volume}")
        self.volume_slider.set(volume)
          
    def volume_down(self,  event=None):
        # Decrease volume by 1 unit
        volume = self.player.audio_get_volume()
        volume -= 1
        self.player.audio_set_volume(volume)
        self.volume_label.config(text=f"{volume}")
        self.volume_slider.set(volume)

    def set_duration(self):
        # Set total duration of current media
        length = self.player.get_length()
        if length > 0:
            self.duration = length
            self.time_slider.config(to=length)
            self.total_time_label.config(text=f"{format_time(length)}")
        else:
            # Retry until duration is available
            self.root.after(500, self.set_duration)
            
    def seek_on_release(self, event):
        # Seek to position when slider is released
        val = self.time_slider.get()
        self.player.set_time(int(val))
            
    def update_time(self):
        # Update current playback time and slider position
        current_time = self.player.get_time()
        
        if current_time > 10 and not self.player.is_playing():
            pass
             
        if self.player.is_playing():
            # Update UI while playing
            self.mp6_label_left.config(image=self.mp6)
            self.mp6_label_right.config(image=self.mp6)
            self.style.configure('Custom.Horizontal.TScale', troughcolor="#8A4A06")#8A4A06
            self.current_time_label.config(fg="#90C87A")
            self.total_time_label.config(fg="#90C87A")
            self.play_pause_button.config(image=self.pause_big)
            if current_time >= 0 and not self.slider_dragging and abs(current_time - self.time_slider.get()) > 500:

                self.updating_slider = True
                self.time_slider.set(current_time)
                self.current_time_label.config(text=format_time(current_time))
                self.updating_slider = False    
        else:
            # Update UI when stopped or paused
            self.mp6_label_left.config(image=self.mp6_off)
            self.mp6_label_right.config(image=self.mp6_off)
            self.style.configure('Custom.Horizontal.TScale', troughcolor="black")
            self.current_time_label.config(fg="#ADADAD")
            self.total_time_label.config(fg="#ADADAD")
            self.play_pause_button.config(image=self.play_off)
            # Handle end of track
            if self.duration > 0 and current_time >= self.duration - 1000:
                if self.loop_enabled:
                    self.play_from_selection()
                else:
                    self.play_next()

        self.root.after(1000, self.update_time)
         
    def seek_to_time(self, seconds):
        # Seek to a specific time in seconds
        self.player.set_time(seconds * 1000)  
         
    def on_slider_press(self, event):
        # Mark slider as being dragged
        self.slider_dragging = True
        
    def on_slider_release(self, event):
        # Release slider and seek to position
        self.slider_dragging = False
        self.seek_on_release(event) 

    def on_slider_move(self, val):
        # Update time label while dragging slider
        if self.slider_dragging:
            seconds = int(float(val))
            self.current_time_label.config(text=format_time(seconds))

    def on_double_click(self, event):
        # Play item on double-click in playlist
        selection = self.listbox.curselection()
        if selection:
            self.current_index = selection[0]
            self.play_from_selection()
            
    def toggle_loop(self):
        # Toggle loop mode
        self.loop_enabled = not self.loop_enabled
        state =  "#065509" if self.loop_enabled else "#3E3838"
        self.loop_button.config(bg=state)

    def toggle_shuffle(self):
        # Toggle shuffle mode
        self.shuffle_enabled = not self.shuffle_enabled
        color = "#065509" if self.shuffle_enabled else "#3E3838"
        self.shuffle_button.config(bg=color)

    def on_drop(self, event):
        # Handle drag-and-drop of files into playlist
        self.listbox.delete(0, tk.END)
        self.playlist.clear()
        self.current_index = None
        files = self.root.tk.splitlist(event.data)
        self.placeholder.place_forget()
        self.logo_listbox.place_forget()

        for btn in self.radio_buttons.values():
            btn.config(bg="#191818")

        if files:
            f = files[0]
            self.playlist = [f]
            self.current_file_is_audio = f.lower().endswith((".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma", ".aiff", ".alac"))
            self.load_media_file(f)

            if self.current_file_is_audio:
                self.show_audio_ui(f)
            else:
                self.show_video_ui(f)

            self.current_index = 0
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.listbox.activate(self.current_index)
            self.play_from_selection()
        self.playlist_button.config(bg="#BC853D")
        
    def embed_video(self):
        # Embed video output into Tkinter frame depending on OS
        video_id = self.video_frame.winfo_id()
        system = platform.system()

        if system == "Windows":
            self.player.set_hwnd(video_id)
        elif system == "Linux":
            self.player.set_xwindow(video_id)
        elif system == "Darwin":
            self.player.set_nsobject(video_id)
        else:
            print("Unsupported system to embed video.")

    def toggle_fullscreen(self):
        # Toggle fullscreen mode for the main window
        self.fullscreen = not getattr(self, "fullscreen", False)
        self.root.attributes("-fullscreen", self.fullscreen)

        if self.fullscreen:
            # Hide UI elements in fullscreen
            self.listbox.grid_remove()
            self.control_frame.grid_remove()
            self.slider.grid_remove()
        else:
            # Restore UI elements when exiting fullscreen
            self.listbox.grid()
            self.control_frame.grid()
            self.slider.grid()

    def hide_eq_ui(self):
        # Hide equalizer UI elements
        self.eq_frame.grid_remove()
        self.eq_light_frame.grid_remove()
        self.eq_line
        for slider in self.eq_sliders:
            slider.grid_remove()
        for label in self.eq_light_labels:
            label.grid_remove()
            
    def show_eq_ui(self):
        # Show equalizer UI elements
        self.eq_frame.grid_remove()
        self.eq_light_frame.grid_remove()
        for i, slider in enumerate(self.eq_sliders):
            slider.grid(row=0, column=i, padx=0)
        for i, label in enumerate(self.eq_light_labels):
            label.grid(row=1, column=i, padx=33)

    def enter_fullscreen_video(self):
        # Enter fullscreen mode for video playback
        if self.current_file_is_audio:
            messagebox.showinfo("Full screen mode", "Full screen mode is disabled for audio files")
            return
        self.original_geometry = self.root.geometry()
        self.hide_eq_ui()
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.main_frame.configure(bg="black")
        self.top_frame.configure(bg="black")
        self.pantlla_completa = True

        # Reconfigure layout for fullscreen video
        self.video_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.top_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")

        for widget in [
            self.black_frame, self.controls_frame, self.central_frame, self.right_frame,
            self.left_frame, self.vu_frame_left, self.vu_frame_right, self.listbox,
            self.time_slider, self.current_time_label, self.total_time_label, self.midle_frame, self.eq_line,
        ]:
            widget.grid_remove()

        # Adjust grid weights for fullscreen
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Start overlay controls
        self.overlay.create_overlay()
        self.overlay.start_slider_update(self.get_current_time, self.get_total_length)
        self.overlay.start_mouse_tracking()
           
    def exit_fullscreen_video(self):
        #Exit fullscreen mode and restore layout
        self.root.attributes("-fullscreen", False) 
        self.root.geometry("600x385")
        
        # Restore UI layout
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.black_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")
        self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.times_frame.grid(row=3, columnspan=5, sticky="nsew")
        self.controls_frame.grid(row=0, column=0, padx=(40,0), pady=(7,0))  
        self.central_frame.grid(row=5, column=2, sticky="n")
        self.right_frame.grid(padx=(0), pady=(0), row=5, column=3, sticky="e")
        self.left_frame.grid(padx=(15,0),pady=(0,10),row=5, column=1)
        self.vu_frame_left.grid(row=5, column=0, padx=15, pady=(0))
        self.vu_frame_right.grid(row=5, column=4, padx=(10), pady=(0))
        self.midle_frame.grid(row=4, columnspan=5, sticky="nsew")
        self.times_frame.grid(row=3, columnspan=5, sticky="nsew")
        self.listbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        
        # Reset colors and background
        self.root.configure(bg="#2C2929")
        self.main_frame.configure(bg="#2C2929")
        self.black_frame.config(bg="#1D1C1B")
        self.current_time_label.grid(row=3, column=0, padx=2, sticky="w")
        self.total_time_label.grid(row=3, column=5, padx=2)
        self.time_slider.grid(row=2, column=0, sticky="nsew")
        self.eq_frame.grid(row=7, columnspan=5)
        self.eq_light_frame.grid(row=8, columnspan=5, padx=(0,21))
        self.hal_label.grid(row=0, column=1, pady=(3,0), sticky="ns")
        self.hal_label.config(bg='#1D1C1B')

        # Destroy overlay and restart EQ UI
        if self.overlay_window:
            self.overlay.destroy_overlay()
        self.root.after(100, self.show_eq_ui)
        self.overlay.stop_mouse_tracking()

    def hide_overlay(self):
        # Hide floating overlay window
        if self.overlay_window:
            self.overlay_window.withdraw()
            
    def track_mouse(self):
        # Track mouse movement to show overlay
        if not self.mouse_tracker_active:
            return  
        x = self.master.winfo_pointerx()
        y = self.master.winfo_pointery()
        current_position = (x, y)
        if self.last_mouse_position != current_position:
            self.last_mouse_position = current_position
            self.show_overlay()
        self.master.after(300, self.track_mouse)

    def breathe_hal(self, index=0, direction=1):
            # Animate HAL logo with breathing effect
            self.hal_label.configure(image=self.hal_frames[index])
            next_index = index + direction
            if next_index == len(self.hal_frames) or next_index < 0:
                    direction *= -1
                    next_index = index + direction
            self.root.after(80, lambda: self.breathe_hal(next_index, direction))
            
    def toggle_mute(self, event=None):
        # Toggle mute state
        if self.is_muted:
            # Restore previous volume
            self.volume_slider.set(self.last_volume)
            self.is_muted = False
            self.volume_label.config(fg="#CAFFFE")
            self.mute_button.config(bg="#191818")
            self.volume_label_frame.config(fg="green")
            self.style.configure('TScale', troughcolor="#AC8433")            
        else:
            # Mute audio
            self.last_volume = self.volume_slider.get()
            self.volume_slider.set(0)
            self.mute_button.config(bg="#D21A1A")
            self.style.configure('TScale', troughcolor="#D21A1A")
            self.is_muted = True

    def load_file_in_listbox(self,ruta):
        # Load audio metadata into playlist listbox
        audio = File(ruta)
        if audio is None:
            self.listbox.insert("end", ruta.split("/")[-1]) 
            return

        duracion = ""
        if hasattr(audio.info, 'length'):
            minutos = int(audio.info.length // 60)
            segundos = int(audio.info.length % 60)
            duracion = f"[{minutos}:{segundos:02d}]"

        titulo = ""
        artista = ""
        if audio.tags:
            if "TIT2" in audio.tags:
                titulo = audio.tags["TIT2"].text[0]
            if "TPE1" in audio.tags:
                artista = audio.tags["TPE1"].text[0]

        if titulo or artista:
            linea = f"{artista} – {titulo} {duracion}"
        else:
            linea = f"{ruta.split('/')[-1]} {duracion}"

        self.listbox.insert("end", linea)

    def compact(self):
        if self.is_compact and not self.eq_t:
            # Toggle compact UI mode
            self.force_layout_refresh()
            self.root.geometry("600x385")
            self.compact_button.config(bg="#191818", text="-/+")
            self.radios_labels.grid(padx=(0), pady=(2,5), row=0)
            self.misc_label.grid(pady=(2,0))
            self.playlist_label.grid(padx=0, pady=(13,0))
            self.eq_button.grid(padx=(0), pady=(5,0))
            self.current_time_label.config(bg="black")
            self.total_time_label.config(bg="black")
            self.times_frame.config(bg="black")
            self.is_compact = False
            print("compact 1")
        elif self.is_compact and self.eq_t:
            self.root.geometry("600x540")
            self.compact_button.config(bg="#191818", text="-/+")
            self.black_frame.grid(column=0, columnspan=5, sticky="nsew")
            self.radios_labels.grid(padx=(0), pady=(2,5), row=0)
            self.misc_label.grid(pady=(2,0))
            self.eq_button.grid(padx=(0), pady=(5,0))
            self.playlist_label.grid(padx=0, pady=(13,0))
            self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew") 
            self.midle_frame.grid()
            self.eq_button.config(bg="#006400")
            self.times_frame.config(bg="black")
            self.top_frame.grid()
            self.current_time_label.config(bg="black", fg="#ADADAD")
            self.total_time_label.config(bg="black", fg="#ADADAD")
            self.current_time_label.grid(row=3, column=0, padx=2, sticky="w")
            self.total_time_label.grid(row=3, column=5, padx=2)
            self.times_frame.grid(row=3, columnspan=5, sticky="nsew")
            self.is_compact = False
            print("compact 2")
        elif self.is_compact and self.eq_t:
            self.root.geometry("600x540")
            self.compact_button.config(bg="#191818", text="-/+")
            self.eq_button.config(bg="#0B0B0B", text="-/+")
            self.black_frame.grid(column=0, columnspan=5, sticky="nsew")
            self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew") 
            self.midle_frame.grid()
            self.times_frame.config(bg="black")
            self.top_frame.grid()
            self.current_time_label.config(bg="black", fg="#ADADAD")
            self.total_time_label.config(bg="black", fg="#ADADAD")
            self.is_compact = False
            print("compact 3")
        
            
        else:
            self.root.geometry("600x140")
            self.compact_button.config(bg="#006400", text="-/+")
            self.top_frame.grid_remove()
            self.midle_frame.grid_remove()
            self.times_frame.config(bg="#2C2929")
            self.top_frame.grid_remove()
            self.black_frame.grid_remove()
            self.eq_button.config(bg="#191818", text="EQ")
            self.current_time_label.config(bg="#2C2929")
            self.total_time_label.config(bg="#2C2929")
            self.controls_frame.grid(pady=0)
            self.radios_labels.grid(pady=(0,5))
            self.eq_button.grid(padx=(0), pady=(5,0))
            self.playlist_label.grid(padx=0, pady=0)
            self.times_frame.grid(row=0, pady=0, columnspan=5, sticky="nsew")
            self.current_time_label.grid(row=0, column=0, padx=2,pady=0, sticky="w")
            self.total_time_label.grid(row=0, column=5, padx=2, pady=0)
            self.is_compact = True
            print("Compact 4")

    def toggle_eq(self):
        # Toggle equalizer UI visibility
        self.eq_t = not self.eq_t
        if self.is_compact:
            if self.eq_t:
                self.root.geometry("600x295")
                self.eq_frame.grid(); self.eq_line.grid(); self.eq_light_frame.grid()
                self.eq_button.config(bg="#006400", text="EQ")
            else:
                self.root.geometry("600x140")
                self.eq_frame.grid_remove(); self.eq_line.grid_remove(); self.eq_light_frame.grid_remove()
                self.eq_button.config(bg="#191818", text="EQ")
        else:
            if self.eq_t:
                self.root.geometry("600x540")
                self.eq_frame.grid(); self.eq_line.grid(); self.eq_light_frame.grid()
                self.eq_button.config(bg="#006400", text="EQ")
            else:
                self.root.geometry("600x385")
                self.eq_frame.grid_remove(); self.eq_line.grid_remove(); self.eq_light_frame.grid_remove()
                self.eq_button.config(bg="#191818", text="EQ")

    def update_eq_lights(self):
        # Update EQ lights depending on playback state
            if hasattr(self, 'player') and self.player:
                    if self.player.is_playing():
                        # Show active EQ lights
                        for label in self.eq_light_labels:
                                label.config(image=self.eq_light_on_image)
                        for slider in self.eq_sliders:
                                slider.config(troughcolor="#36E014")
                    else:
                        # Show inactive EQ lights
                        for label in self.eq_light_labels:
                                label.config(image=self.eq_light_image)
                        for slider in self.eq_sliders:
                                slider.config(troughcolor="#0D0D0D")
                                
    def start_eq_light_loop(self):
        # Continuously update EQ lights every second
        self.update_eq_lights()
        self.root.after(1000, self.start_eq_light_loop)  

    def on_slider_change(self, val, idx):
        # Handle EQ slider change and update equalizer band
        val = float(val)
        current_val = self.eq.get_amp_at_index(idx)
        if abs(current_val - val) >= 1:
            self.eq.set_amp_at_index(val, idx)
            self.root.after(200, self.apply_eq_to_player)

    def apply_eq_to_player(self):
        # Apply the current equalizer settings to the VLC player
        if self.player:
            self.player.set_equalizer(self.eq)
            
    def init_eq(self):
        # Prevents audio cut on first EQ adjustment
        self.on_slider_change(1, 1)

    def toggle_play_pause(self, event=None):
        # Toggle between play and pause states
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

    def get_current_time(self):
        # Return current playback time in seconds
        return int(self.player.get_time() / 1000) 

    def get_total_length(self):
        # Return total media length in seconds
        return int(self.player.get_length() / 1000)  

    def play(self):
        self.player.play()
           
    def pause(self):
        self.player.pause()
        
    def show_hotkeys(self, event=None):
        # Display a window with available keyboard shortcuts
        hotkey_window = tk.Toplevel(self.root)
        hotkey_window.title("Hotkeys")
        hotkey_window.geometry("300x200")
        hotkey_window.configure(bg="#191818")
        hotkey_window.resizable(False, False)

        tk.Label(hotkey_window, text="PLAYER HOTKEYS", fg="#36AF1D", bg="#161515", font=("Terminal", 12)).pack(pady=10)

        hotkeys = [
            "␣  Space: Play / Pause",
            "←  Left: Skip back",
            "→  Right: Skip forward",
            "↑  Up: Volume up",
            "↓  Down: Volume down",
            "H: Show hotkeys",
            "M: Mute"
        ]

        for key in hotkeys:
            tk.Label(hotkey_window, text=key, fg="#ADADAD", bg="#161515", font=("Lucida Console", 11)).pack(anchor="w", padx=20)

    def play_radio(self, name):
        # Play a radio stream by name from the radios dictionary
        self.play_pause_button.config(image=self.pause_big)
        self.placeholder.place_forget()
        self.logo_listbox.place_forget()
        self.listbox.delete(0, tk.END)
        self.playlist_button.config(bg="#BC853D")
        url = self.radios[name]

        # Reset button colors and highlight selected radio
        for btn in self.radio_buttons.values():
            btn.config(bg="#006400")
        self.radio_buttons[name].config(bg="#359635")

        # Show radio placeholder image
        self.placeholder.place(relx=0.5, rely=0.7, anchor="center")
        # Start radio playback
        media = self.vlc_instance.media_new(url)
        self.player.set_media(media)
        self.player.play()
        self.show_radio_image()

    def load_current_playlist(self):
        archivo = filedialog.askopenfilename(
            title="Load playlist",
            filetypes=[("Text files", "*.txt")]
        )

        # Reset UI
        self.placeholder.place_forget()
        self.logo_listbox.place_forget()
        self.listbox.delete(0, tk.END)

        if archivo:
            try:
                rutas = playlist_manager.load_playlist(archivo)

                if not rutas:
                    messagebox.showwarning("Lista vacía", "La lista seleccionada no contiene archivos.")
                    return

                self.playlist = rutas

                # Add files to listbox with metadata if audio
                for f in self.playlist:
                    self.current_file_is_audio = f.lower().endswith((".mp3", ".wav", ".flac"))
                    if self.current_file_is_audio:
                        self.video_frame.grid_remove()
                        self.listbox.grid(row=1, column=0, sticky="nsew")
                        self.listbox.lift()
                        self.load_file_in_listbox(f)
                        self.playlist_button.config(bg="#006400")
                    else:
                        self.listbox.insert(tk.END, os.path.basename(f))

                # Reset radio button colors
                for btn in self.radio_buttons.values():
                    btn.config(bg="#191818")

                # Select first item and start playback
                self.current_index = 0
                self.listbox.selection_set(0)
                self.listbox.activate(0)
                self.play_from_selection()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la lista:\n{e}")
                
    def create_new_playlist(self):
        archivo = filedialog.asksaveasfilename(
            title="Create new playlist",
            initialfile="new_list.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if archivo:
            try:
                playlist_manager.create_playlist(archivo)
                messagebox.showinfo("List created", f"The list was created:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"The list could not be created:\n{e}")
                
    def add_to_playlist(self):
        pass
    
    def add_to_existing_playlist(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar lista para agregar",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if archivo:
            try:
                new, repeated = playlist_manager.add_to_playlist(archivo, self.playlist)

                if new:
                    messagebox.showinfo("Updated list", f"They were added {len(new)} files to:\n{archivo}")
                if repeated:
                    messagebox.showwarning("Duplicados", f"{len(repeated)} files were already in the list and were not added.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not be added to the list:\n{e}")
            
    def show_audio_ui(self, f):
        # Configure UI for audio playback
        self.video_frame.grid_remove()
        self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.listbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.top_frame.configure(bg='#191818')
        self.load_file_in_listbox(f)
        self.listbox.lift()
        self.listbox.update_idletasks()
        self.root.update_idletasks()

    def show_video_ui(self, f):
        # Configure UI for video playback
        self.video_frame.lift()
        self.black_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")
        self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.video_frame.grid(row=0, column=0, sticky="nsew") 
        self.listbox.insert(tk.END, os.path.basename(f))
        print(self.black_frame.grid_info())
        self.force_layout_refresh()
        
    def load_media_file(self, f):
        # Load a media file into the VLC player
        media = self.vlc_instance.media_new(f)
        self.player.set_media(media)
        
    def force_layout_refresh(self):
        # Force UI refresh by temporarily exiting fullscreen
        self.root.after(50, self.exit_fullscreen_video)

    def show_radio_image(self):
        if not self.is_compact:
            self.listbox.lift()
        self.placeholder.config(image=self.radio_image)



        
        
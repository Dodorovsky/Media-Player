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

class PlaylistPlayer:
    def __init__(self, root):
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

        self.eq.set_preamp(10.0)
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
        self.pausa = False
        self.stopp = False
        self.playy = False
        self.is_muted = False
        self.last_volume = 50
        self.is_compact = False
        self.eq_t = False
        self.subtitles_path = None
        self.slider_dragging = False
 
        self.eq_color = "eq_light"
        
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
        self.listbox.bind("<Double-Button-1>", self.on_double_click)
        self.time_slider.bind("<ButtonPress-1>", self.on_slider_press)
        self.time_slider.bind("<ButtonRelease-1>", self.on_slider_release)

    def load_files(self):
        files = filedialog.askopenfilenames()
        self.stop_button.config(image=self.stop_off)
        self.placeholder.place_forget()
        self.logo_listbox.place_forget()
        self.player.stop()
        self.player.release()
        self.player = self.vlc_instance.media_player_new()

        for btn in self.radio_buttons.values():
            btn.config(bg="#191818")
        if files:
            self.playlist = list(files)
            self.listbox.delete(0, tk.END)
            for f in self.playlist:
                self.current_file_is_audio = f.lower().endswith((".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma", ".aiff", ".alac"))
                if self.current_file_is_audio:
                    self.video_frame.grid_remove()
                    self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
                    self.listbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew") 
                    self.top_frame.configure(bg='#181717')
                    self.load_file_in_listbox(f)                 
                else:
                    self.listbox.insert(tk.END, os.path.basename(f))
              
            self.pantlla_completa =False
            self.current_index = 0
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.play_from_selection()
        self.playlist_button.config(bg="#BC853D")
        
    def play_from_selection(self):
        if self.current_index is None:
            print("Kein Element in der Playlist ausgewählt.")
            return
        
        filepath = self.playlist[self.current_index]

        media = self.vlc_instance.media_new(filepath)
        auto_sub = Path(filepath).with_suffix(".srt")
        if self.subtitles_path:
            ruta_sub = Path(self.subtitles_path).as_posix()
            media.add_option(f'sub-file="{ruta_sub}"') 
        self.player.set_media(media)

        self.player.play()
        
        if filepath.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
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
            
        if self.pantlla_completa:
            self.video_frame.grid(row=0, column=0, sticky="nsew")
            self.video_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
                        
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
        selection = self.listbox.curselection()
        media = self.player.get_media()
        if not selection and not media:
            return
        if self.player.is_playing():
            self.player.pause()  
            self.play_pause_button.config(image=self.play_off)
        else:
            state = self.player.get_state()
            self.play_pause_button.config(image=self.pause_big)
            self.player.play()
            if state == vlc.State.Paused:
                self.play_pause_button.config(image=self.pause_big)
                self.player.play()
           
    def stop(self):
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
        if self.current_index is not None and self.current_index > 0:
            self.current_index -= 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.listbox.activate(self.current_index)
            self.play_from_selection()

    def play_next(self, event=None):
        if not self.playlist:
            return
        
        if self.shuffle_enabled:
            next_index = random.randint(0, len(self.playlist) - 1)

            while next_index == self.current_index and len(self.playlist) > 1:
                next_index = random.randint(0, len(self.playlist) - 1)
            self.current_index = next_index
        else:
            if self.current_index is not None and self.current_index < len(self.playlist) - 1:
                self.current_index += 1
            else:
                return  

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.current_index)
        self.listbox.activate(self.current_index)
        self.play_from_selection()
      
    def set_volume(self, val):
        vol = int(float(val))
        self.player.audio_set_volume(vol)
        self.volume_label.config(text=f"{vol}")
        if vol > 1 and self.is_muted:
            self.volume_label.config(fg="#CAFFFE")
            self.mute_button.config(bg="#3E3838")
            self.volume_label_frame.config(fg="green")
            self.style.configure('TScale', troughcolor="#AC8433")
            self.is_muted = False
        elif vol < 1 and not self.is_muted:
            self.mute_button.config(bg="#D21A1A")
            self.style.configure('TScale', troughcolor="#D21A1A")
            self.is_muted = True
        
    def volume_up(self,  event=None):
        volume = self.player.audio_get_volume()
        volume += 1
        self.player.audio_set_volume(volume)
        self.volume_label.config(text=f"{volume}")
        self.volume_slider.set(volume)
        
    def volume_down(self,  event=None):
        volume = self.player.audio_get_volume()
        volume -= 1
        self.player.audio_set_volume(volume)
        self.volume_label.config(text=f"{volume}")
        self.volume_slider.set(volume)
        
    def set_duration(self):
        length = self.player.get_length()
        if length > 0:
            self.duration = length
            self.time_slider.config(to=length)
            self.total_time_label.config(text=f"{format_time(length)}")
        else:
            self.root.after(500, self.set_duration)

    def seek_on_release(self, event):
        val = self.time_slider.get()
        self.player.set_time(int(val))
            
    def update_time(self):
        current_time = self.player.get_time()
        
        if current_time > 10 and not self.player.is_playing():
            pass
             
        if self.player.is_playing():
            self.mp6_label_left.config(image=self.mp6)
            self.mp6_label_right.config(image=self.mp6)
            self.style.configure('Custom.Horizontal.TScale', troughcolor="#8A4A06")#8A4A06
            self.current_time_label.config(fg="#90C87A")
            self.total_time_label.config(fg="#90C87A")
            if current_time >= 0 and not self.slider_dragging and abs(current_time - self.time_slider.get()) > 500:

                self.updating_slider = True
                self.time_slider.set(current_time)
                self.current_time_label.config(text=format_time(current_time))
                self.updating_slider = False    
        else:
            self.mp6_label_left.config(image=self.mp6_off)
            self.mp6_label_right.config(image=self.mp6_off)
            self.style.configure('Custom.Horizontal.TScale', troughcolor="black")
            self.current_time_label.config(fg="#ADADAD")
            self.total_time_label.config(fg="#ADADAD")
    
            if self.duration > 0 and current_time >= self.duration - 1000:
                if self.loop_enabled:
                    self.play_from_selection()
                else:
                    self.play_next()

        self.root.after(1000, self.update_time)
         
    def seek_to_time(self, seconds):
        self.player.set_time(seconds * 1000)  
        
    def on_slider_press(self, event):
        self.slider_dragging = True

    def on_slider_release(self, event):
        self.slider_dragging = False
        self.seek_on_release(event) 

    def on_slider_move(self, val):
        if self.slider_dragging:
            seconds = int(float(val))
            self.current_time_label.config(text=format_time(seconds))

    def on_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.current_index = selection[0]
            self.play_from_selection()
            
    def toggle_loop(self):
        self.loop_enabled = not self.loop_enabled
        state =  "#065509" if self.loop_enabled else "#3E3838"
        self.loop_button.config(bg=state)

    def toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled
        color = "#065509" if self.shuffle_enabled else "#3E3838"
        self.shuffle_button.config(bg=color)

    def on_drop(self, event):
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

    def hide_eq_ui(self):
        self.eq_frame.grid_remove()
        self.eq_light_frame.grid_remove()
        self.eq_line
        for slider in self.eq_sliders:
            slider.grid_remove()

        for label in self.eq_light_labels:
            label.grid_remove()
            
    def show_eq_ui(self):
        self.eq_frame.grid_remove()
        self.eq_light_frame.grid_remove()
        for i, slider in enumerate(self.eq_sliders):
            slider.grid(row=0, column=i, padx=0)
        for i, label in enumerate(self.eq_light_labels):
            label.grid(row=1, column=i, padx=33)

    def enter_fullscreen_video(self):
        print("enter_fullscreen called")
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

        self.video_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.top_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")

        for widget in [
            self.black_frame, self.controls_frame, self.central_frame, self.right_frame,
            self.left_frame, self.vu_frame_left, self.vu_frame_right, self.listbox,
            self.time_slider, self.current_time_label, self.total_time_label, self.midle_frame, self.eq_line,
        ]:
            widget.grid_remove()

        self.main_frame.grid_rowconfigure(1, weight=0, minsize=0)
        self.main_frame.grid_rowconfigure(2, weight=0, minsize=0)
        self.top_frame.grid_rowconfigure(0, weight=0, minsize=0)
        self.top_frame.grid_rowconfigure(2, weight=0, minsize=0)
        self.top_frame.grid_rowconfigure(3, weight=0, minsize=0)
        
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=0)
        self.main_frame.grid_columnconfigure(4, weight=0)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.overlay.create_overlay()
        self.overlay.start_slider_update(self.get_current_time, self.get_total_length)

        self.overlay.start_mouse_tracking()
        
    def exit_fullscreen_video(self):
        self.root.attributes("-fullscreen", False) 
        self.root.geometry("600x383")
        
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
        
        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1) 
        self.main_frame.grid_columnconfigure(2, weight=2)
        
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(2, weight=1)
        self.top_frame.grid_rowconfigure(3, weight=1)

        self.root.configure(bg="#2C2929")
        self.main_frame.configure(bg="#2C2929")
        self.top_frame.grid_rowconfigure(0, weight=0)
        self.top_frame.grid_rowconfigure(1, weight=1) 
        self.top_frame.grid_rowconfigure(2, weight=0)
        self.top_frame.grid_rowconfigure(3, weight=0)
        self.top_frame.grid_columnconfigure(0, weight=1)
        
        self.black_frame.grid_columnconfigure(0, weight=1)
        self.black_frame.grid_columnconfigure(1, weight=1) 
        self.black_frame.grid_columnconfigure(2, weight=1)
        self.black_frame.grid_rowconfigure(0, minsize=25)

        self.black_frame.config(bg="#1D1C1B")
        self.current_time_label.grid(row=3, column=0, padx=2, sticky="w")
        self.total_time_label.grid(row=3, column=5, padx=2)
        self.time_slider.grid(row=2, column=0, padx=0, sticky="nsew")
        self.eq_frame.grid(row=7, columnspan=5)
        self.eq_light_frame.grid(row=8, columnspan=5, padx=(0,21))
        self.hal_label.grid(row=0, column=1, pady=(3,0), sticky="ns")
        self.hal_label.config(bg='#1D1C1B')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        if self.overlay_window:
            self.overlay.destroy_overlay()
        self.root.after(100, self.show_eq_ui)
        self.overlay.stop_mouse_tracking()

    def hide_overlay(self):
        if self.overlay_window:
            self.overlay_window.withdraw()
            
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

    def breathe_hal(self, index=0, direction=1):
            self.hal_label.configure(image=self.hal_frames[index])
            next_index = index + direction
            if next_index == len(self.hal_frames) or next_index < 0:
                    direction *= -1
                    next_index = index + direction
            self.root.after(80, lambda: self.breathe_hal(next_index, direction))

    def toggle_mute(self, event=None):
        volume = self.player.audio_get_volume()
        if self.is_muted:
            self.volume_slider.set(self.last_volume)
            self.is_muted = False
            self.volume_label.config(fg="#CAFFFE")
            self.mute_button.config(bg="#191818")
            self.volume_label_frame.config(fg="green")
            self.style.configure('TScale', troughcolor="#AC8433")
            self.current_time_label.config(fg="#E58D8D")
            self.total_time_label.config(fg="#E58D8D")
                
        else:
            self.last_volume = self.volume_slider.get()
            self.volume_slider.set(0)
            self.mute_button.config(bg="#D21A1A")
            self.style.configure('TScale', troughcolor="#D21A1A")
            self.is_muted = True

    def load_file_in_listbox(self,ruta):
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
            self.force_layout_refresh()
            self.root.geometry("600x383")
            self.compact_button.config(bg="#191818", text="-/+")
            self.radios_labels.grid(padx=(0), pady=(8,5), row=0)
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
            self.radios_labels.grid(padx=(0), pady=(8,5), row=0)
            self.eq_button.grid(padx=(0), pady=(20,0))
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
            self.radios_labels.grid(pady=0)
            self.eq_button.grid(padx=(0), pady=0)
            self.playlist_label.grid(padx=0, pady=0)
            self.times_frame.grid(row=0, pady=0, columnspan=5, sticky="nsew")
            self.current_time_label.grid(row=0, column=0, padx=2,pady=0, sticky="w")
            self.total_time_label.grid(row=0, column=5, padx=2, pady=0)
            self.is_compact = True
            print("Compact 4")
    def toggle_eq(self):
        if self.eq_t and not self.is_compact:
                    self.root.geometry("600x383")
                    self.eq_button.config(bg="#191818", text="EQ")
                    self.eq_frame.grid_remove()
                    self.eq_line.grid_remove()
                    self.eq_light_frame.grid_remove()
                    self.eq_t = False
                    print("1")
        elif not self.eq_t and not self.is_compact:
            
                    self.root.geometry("600x540")
                    self.eq_button.config(bg="#006400")
                    self.eq_frame.grid()
                    self.eq_line.grid()
                    self.eq_light_frame.grid()
                    self.eq_t = True
                    print("2")
        elif self.eq_t and self.is_compact:
                    self.root.geometry("600x140")
                    self.eq_button.config(bg="#191818", text="EQ")
                    self.eq_frame.grid_remove()
                    self.eq_line.grid_remove()
                    self.eq_light_frame.grid_remove()
                    self.eq_t = False
                    print("3")
        elif not self.eq_t and self.is_compact:
                    self.root.geometry("600x295")
                    self.eq_button.config(bg="#006400", text="EQ")
                    self.eq_frame.grid()
                    self.eq_line.grid()
                    self.eq_light_frame.grid()
                    self.eq_t = True
                    print("4")

    def update_eq_lights(self):
            if hasattr(self, 'player') and self.player:
                    if self.player.is_playing():
                            for label in self.eq_light_labels:
                                    label.config(image=self.eq_light_on_image)
                            for slider in self.eq_sliders:
                                    slider.config(troughcolor="#36E014")
                    else:
                            for label in self.eq_light_labels:
                                    label.config(image=self.eq_light_image)
                            for slider in self.eq_sliders:
                                    slider.config(troughcolor="#0D0D0D")
                                
    def start_eq_light_loop(self):
            self.update_eq_lights()
            self.root.after(1000, self.start_eq_light_loop)  

    def on_slider_change(self, val, idx):
        val = float(val)
        current_val = self.eq.get_amp_at_index(idx)
        if abs(current_val - val) >= 1:
            self.eq.set_amp_at_index(val, idx)
            self.root.after(200, self.apply_eq_to_player)

    def apply_eq_to_player(self):
        if self.player:
            self.player.set_equalizer(self.eq)

    def toggle_play_pause(self, event=None):
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

    def get_current_time(self):
        return int(self.player.get_time() / 1000) 

    def get_total_length(self):
        return int(self.player.get_length() / 1000)  

    def play(self):
        self.player.play()
           
    def pause(self):
        self.player.pause()   
         
    def show_hotkeys(self, event=None):
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
        self.play_pause_button.config(image=self.pause_big)
        self.placeholder.place_forget()
        self.logo_listbox.place_forget()
        self.listbox.delete(0, tk.END)
        self.playlist_button.config(bg="#BC853D")

        url = self.radios[name]

        for btn in self.radio_buttons.values():
            btn.config(bg="#006400")

        self.radio_buttons[name].config(bg="#359635")
        self.placeholder.config(image=self.radio_image)
        self.placeholder.place(relx=0.5, rely=0.7, anchor="center")
    
        media = self.vlc_instance.media_new(url)
        self.player.set_media(media)
        self.player.play()
        self.force_layout_refresh()

    def create_playlist(self):
        archivo = filedialog.asksaveasfilename(
            title="Crear nueva lista de reproducción",
            initialfile="nueva_lista.txt",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if archivo:
            try:
                with open(archivo, "w", encoding="utf-8") as f:
                    pass  
                messagebox.showinfo("Lista creada", f"Se creó la lista:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear la lista:\n{e}")

    def add_to_playlist(self):
        
        archivo = filedialog.askopenfilename(
            title="Seleccionar lista para agregar",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if archivo:
            try:
                with open(archivo, "a", encoding="utf-8") as f:
                    for ruta in self.playlist:
                        f.write(ruta + "\n")
                messagebox.showinfo("Lista actualizada", f"Se agregaron archivos a:\n{archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar a la lista:\n{e}")

    def load_playlist(self):
        archivo = filedialog.askopenfilename(
            title="Cargar lista de reproducción",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        self.placeholder.place_forget()
        self.logo_listbox.place_forget()
        self.listbox.delete(0, tk.END)
        nombre_lista = os.path.basename(archivo)

        if archivo:
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    rutas = [linea.strip() for linea in f if linea.strip()]
                
                if not rutas:
                    messagebox.showwarning("Lista vacía", "La lista seleccionada no contiene archivos.")
                    return

                self.playlist = rutas
                self.listbox.delete(0, tk.END)

                for f in self.playlist:
                    self.current_file_is_audio = f.lower().endswith((".mp3", ".wav", ".flac"))
                    if self.current_file_is_audio:
                        self.load_file_in_listbox(f)
                        self.playlist_button.config(bg="#006400")
                    else:
                        self.listbox.insert(tk.END, os.path.basename(f))
                for btn in self.radio_buttons.values():
                    btn.config(bg="#191818")
                self.current_index = 0
                self.listbox.selection_set(0)
                self.listbox.activate(0)
                self.play_from_selection()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la lista:\n{e}")
            
    def show_audio_ui(self, f):
        self.video_frame.grid_remove()
        self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.listbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.top_frame.configure(bg='#191818')
        self.load_file_in_listbox(f)
        self.listbox.lift()
        self.listbox.update_idletasks()
        self.root.update_idletasks()

    def show_video_ui(self, f):

        self.video_frame.lift()
        self.black_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")
        self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.video_frame.grid(row=0, column=0, sticky="nsew") 
        self.listbox.insert(tk.END, os.path.basename(f))
        print(self.black_frame.grid_info())
        self.force_layout_refresh()
        
    def load_media_file(self, f):
        media = self.vlc_instance.media_new(f)
        self.player.set_media(media)
        
    def force_layout_refresh(self):
        self.root.after(50, self.exit_fullscreen_video)




        
        
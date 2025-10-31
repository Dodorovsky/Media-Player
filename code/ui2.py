from tkinter import PhotoImage
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import vlc 
import os
from modules.vumeter_real import RealVUMeter


def setup_ui(self):
        self.root.title("Reproductor con lista")
        self.root.configure(bg="#82726D")
        self.root.geometry("600x490")
        self.root.title("1979_MODEL  ___  media_player >> by DODOROVSKY")
        self.root.iconbitmap('media_player/graphics/backgrounds/dodorovsky.ico')
        
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg='#3C3A3A')
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)


        # Top Frame for Video and Listbox
        self.top_frame = tk.Frame(self.main_frame, bg='#3C3A3A')
        self.top_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        
        self.top_frame.grid_rowconfigure(1, weight=1)  # vídeo
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(self.top_frame, bg="black", fg="#197F0F", width=110, height=18, selectbackground="#267227", selectforeground="lime")
        self.listbox.grid(row=1, column=0, padx=0, pady=0)      
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)
        
        self.video_frame = tk.Frame(self.top_frame, width=450, height=360, bg="black")
        self.video_frame.grid(row=1, column=0, padx=0, pady=(20, 0), sticky="nsew")
        self.video_frame.drop_target_register(DND_FILES)
        self.video_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.video_frame.grid_forget()
        
        # Time slider and labels
        style = ttk.Style()
        style.configure('TScale', background="#82270E" )
        style.theme_use('clam')  # o 'alt', 'default', 'classic', clam
        
        self.time_slider = ttk.Scale(self.top_frame, from_=0, to=100, orient="horizontal", value=0, length=700, style="TScale")# 664
        self.time_slider.grid(row=2, column=0, padx=0, sticky="nsew")
        
        self.current_time_label = tk.Label(self.top_frame, text="--:--", font=("Terminal", 9), fg="#B92008", bg='#3C3A3A')
        self.current_time_label.grid(row=3, column=0, padx=(0, 540))
        self.total_time_label = tk.Label(self.top_frame, text="--:--", font=("Terminal", 9), fg="#B92008", bg='#3C3A3A')
        self.total_time_label.grid(row=3, column=0, padx=(540, 0))
        
        # Vumeter Frame
        self.vu_frame = tk.Frame(self.main_frame, bg='#3C3A3A')
        self.vu_frame.grid(row=2, column=0, sticky="nsew")
        
        # Left Frame
        self.left_frame = tk.Frame(self.main_frame, bg='#3C3A3A')
        self.left_frame.grid(row=2, column=1, sticky="w")
        
        # Central Frame
        self.central_frame = tk.Frame(self.main_frame, bg='#3C3A3A')
        self.central_frame.grid(row=2, column=2, sticky="w")
        
        # Right Frame
        self.right_frame = tk.Frame(self.main_frame, bg='#3C3A3A')
        self.right_frame.grid(row=2, column=3, sticky="nsew")
        
        # Load button label-Frame
        self.load_label_frame = tk.LabelFrame(self.left_frame, text='LOAD', font=("Terminal", 8), bg="#3C3A3A", fg="#F2E7E3")#fg="#E1B19E"
        self.load_label_frame.grid(row=0, column=0, padx=(0, 0), pady=10)
        
        # Load Button
        self.load_button = tk.Button(self.load_label_frame, command=self.load_files, bg="#F0C74C")
        self.load_button.grid(padx=(12, 0), pady=10)
        
        # Loop Button
        self.loop_button = tk.Button(self.left_frame, text="LOOP", font=("Terminal", 8), bg="#D8CDC0", command=self.toggle_loop)#C2DDAC, C4A98A
        self.loop_button.grid(padx=(0, 0), pady=(10,0))
        
        # Random Button
        self.shuffle_button = tk.Button(self.left_frame, text="RANDOM", font=("Terminal", 8), bg="#D8CDC0", command=self.toggle_shuffle)
        self.shuffle_button.grid(padx=(0,0), pady=(5,0))
        
        # Control Labels
        self.label_pause = tk.Label(self.central_frame, fg="#EDE8E6", text="PAUSE", font=("Terminal", 8), bg='#3C3A3A')
        self.label_pause.grid(row=0, column=0, padx=0, pady=(5,0))
        self.label_stop = tk.Label(self.central_frame, text="STOP", fg="#EDE8E6",  font=("Terminal", 8),bg='#3C3A3A')
        self.label_stop.grid(row=0, column=1, padx=0,pady=(5,0))
        self.label_play = tk.Label(self.central_frame, text="PLAY", font=("Terminal", 8), fg="#EDE8E6", bg='#3C3A3A')
        self.label_play.grid(row=0, column=2, padx=1, pady=(5,0))
        
        self.prev_label = tk.Label(self.central_frame, text="PREV", fg="#EDE8E6", font=("Terminal", 8), bg='#3C3A3A')
        self.prev_label.grid(row=2, columnspan=3, padx=0, pady=(5, 0))
        self.next_label = tk.Label(self.central_frame, text="NEXT", fg="#EDE8E6",font=("Terminal", 8), bg='#3C3A3A')
        self.next_label.grid(row=2, columnspan=3, padx=(80,0), pady=(5, 0))
        
        # Define Control Images
        self.play_btn_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/play.png').resize((70, 20)))       
        self.pause_btn_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/pause.png').resize((35,20)))
        self.stop_btn_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/stop.png').resize((35,20)))
        self.previous_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/prev.png').resize((40,8)))
        self.next_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/next.png').resize((40,8)))
        self.power_light_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/power_light.png').resize((20, 20)))


        

        self.power_on_label = tk.Label(self.top_frame,  text="POWER__", font=("terminal", 6), fg="#E9E4B2", bg='#3C3A3A')
        self.power_on_label.grid(row=0, column=0, padx=(0,65) )
        self.power_label_img = tk.Label(self.top_frame, image=self.power_light_img, bg='#3C3A3A')
        self.power_label_img.grid(row=0, column=0, padx=0, pady=5)
        
        # Control Buttons
        self.pause_button = tk.Button(self.central_frame, image=self.pause_btn_img, command=self.pause)
        self.pause_button.grid(row=1, column=0, padx=(10,0))
        
        self.stop_button = tk.Button(self.central_frame, image=self.stop_btn_img, command=self.stop)
        self.stop_button.grid(row=1, column=1, padx=(0,3)) 
        
        self.play_button = tk.Button(self.central_frame, image=self.play_btn_img, command=self.play_from_selection)
        self.play_button.grid(row=1, column=2, padx=0)

        self.prev_button = tk.Button(self.central_frame, image=self.previous_img, command=self.play_previous)
        self.prev_button.grid(row=3, columnspan=3,padx=(0,30))

        self.next_button = tk.Button(self.central_frame, image=self.next_img, command=self.play_next)
        self.next_button.grid( row=3, columnspan=3, padx=(60,0))
        
        
        # Volume Slider label-Frame
        self.volume_label_frame = tk.LabelFrame(self.right_frame, text='VOLUME', font=("Terminal", 8), bg="#3C3A3A", fg="#EDEBDD")#fg="#E1B19E"
        self.volume_label_frame.grid(row=0, column=1, padx=0)

        # Volume Labels
        self.volume_label = tk.Label(self.right_frame, text="50", bg='#3C3A3A', fg="#F3DF98")
        self.volume_label.grid( row=0, column=3, padx=(0,35), pady=(0,110))

        # Volume SLider
        self.volume_slider =  ttk.Scale(self.volume_label_frame, from_=100, to=1, orient="vertical", command=self.set_volume, length=110, style="TScale")
        self.volume_slider.grid(padx=(15, 0), pady=5)
        self.volume_slider.set(50)
        

        
        # Meter Label
        meter_label = tk.Label(self.right_frame, text="______\n _____\n____\n___\n__\n_\n.", bg='#3C3A3A', fg="#E7D3B0")
        meter_label.grid(row=0, column=3, padx=(5,40), pady=(10,0))
        
        self.fullscreen_button = tk.Button(self.central_frame, text="FULL-SCREEN\n\n VIDEO", font=("Terminal", 8), command=self.enter_fullscreen_video, bg="#BDCCD6")##F7EAC3
        self.fullscreen_button.grid(row=4, columnspan=3, padx=(10,0), pady=(15, 0))
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen_video())
        
        self.vumeter = RealVUMeter(self.vu_frame, device_id=1)
        self.vumeter.grid(row=0, column=0, padx=(50, 0), pady=(10,2))

        def update_vumeter():
                
                self.root.after(500, update_vumeter)

        update_vumeter()




        
        
        
        
        
        
        
        
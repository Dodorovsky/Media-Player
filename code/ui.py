from tkinter import PhotoImage
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import vlc 
import os
#from modules.vumeter_real import RealVUMeter
#from modules.vu_meter_experiment import VUMeterExperimental
from modules.vu_meter_experiment import VUColumn

def setup_ui(self):
        self.root.title("Reproductor con lista")
        self.root.configure(bg="#82726D")
        self.root.geometry("600x470")
        self.root.title("->- 9000 MEDI/\ PL/\YER")
        self.root.iconbitmap('media_player/graphics/backgrounds/dodorovsky.ico')
        
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg='#3A3535')
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Top Frame for Video and Listbox
        self.top_frame = tk.Frame(self.main_frame, bg="#3A3535")
        self.top_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")
        
        self.black_frame = tk.Frame(self.top_frame, bg="#232321")##232121
        self.black_frame.grid( sticky="nsew")
        
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_rowconfigure(2, weight=1)
        self.top_frame.grid_rowconfigure(3, weight=1)# vídeo
        
        self.top_frame.grid_columnconfigure(0, weight=1)
        

        self.listbox = tk.Listbox(self.top_frame, bg="black", fg="#197F0F", width=110, height=16, selectbackground="#267227", selectforeground="lime",bd=0, highlightthickness=0, relief="flat")
        self.listbox.grid(row=1, column=0, padx=0, pady=0)      
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)
        
        self.video_frame = tk.Frame(self.top_frame, width=450, height=257, bg="black")# width=450, height=340
        self.video_frame.grid(row=1, column=0, sticky="nsew")
        self.video_frame.drop_target_register(DND_FILES)
        self.video_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.video_frame.grid_forget()
        
        # Time slider and labels
        style = ttk.Style()
        style.configure('TScale', background="#82270E" )
        style.theme_use('clam')  # o 'alt', 'default', 'classic', clam
        
        self.time_slider = ttk.Scale(self.top_frame, from_=0, to=100, orient="horizontal", value=0, length=700, style="TScale")# 664
        self.time_slider.grid(row=2, column=0, padx=0, sticky="nsew")
        
        self.current_time_label = tk.Label(self.top_frame, text="--:--", font=("Terminal", 9), fg="#E9E4B2", bg='#3A3535')
        self.current_time_label.grid(row=3, column=0, padx=(0, 540))
        self.total_time_label = tk.Label(self.top_frame, text="--:--", font=("Terminal", 9), fg="#E9E4B2", bg='#3A3535')
        self.total_time_label.grid(row=3, column=0, padx=(540, 0))
        
        # Vumeter Frame
        self.vu_frame_left = tk.Frame(self.main_frame, bg='#3A3535')
        self.vu_frame_right = tk.Frame(self.main_frame, bg='#3A3535')
        
        self.vu_frame_left.grid(row=2, column=0, padx=0, sticky="w")
        self.vu_frame_right.grid(row=2, column=4, sticky="e")
        
        # Left Frame
        self.left_frame = tk.Frame(self.main_frame, bg="#3A3535")
        self.left_frame.grid(row=2, column=1, sticky="w")
        
        # Central Frame
        self.central_frame = tk.Frame(self.main_frame, bg='#3A3535')
        self.central_frame.grid(row=2, column=2, sticky="nw")
        
        # Right Frame
        self.right_frame = tk.Frame(self.main_frame, bg='#3A3535')
        self.right_frame.grid(row=2, column=3, sticky="nswe")
        
        # Controls Frame
        self.controls_frame = tk.LabelFrame(self.central_frame, text='CONTROLS->- ', font=("Terminal", 8), bg="#3A3535", fg="green")#fg="#E1B19E",  labelanchor="n",
        self.controls_frame.grid(row=0, column=1, padx=(30, 0), pady=(5,0))
        # Load button label-Frame
        self.load_label_frame = tk.Label(self.left_frame, text='LOAD', font=("Terminal", 8), bg="#3A3535", fg="green")#fg="#E1B19E"
        self.load_label_frame.grid(padx=(25,0), pady=(5,0))
        
        # Load Button
        self.load_button = tk.Button(self.left_frame, command=self.load_files, bg="#F0C74C")
        self.load_button.grid(padx=(25,0),pady=5)
        
        # Control Labels
        #self.label_pause = tk.Label(self.central_frame, fg="#EDE8E6", text="PAUSE", font=("Terminal", 8), bg='#3A3535')
        #self.label_pause.grid(row=0, column=0, padx=(8,0), pady=(10,0))
        #self.label_stop = tk.Label(self.central_frame, text="STOP", fg="#EDE8E6",  font=("Terminal", 8),bg='#3A3535')
        #self.label_stop.grid(row=0, column=1, padx=(0,3),pady=(10,0))
        #self.label_play = tk.Label(self.central_frame, text="PLAY", font=("Terminal", 8), fg="#EDE8E6", bg='#3A3535')
        #self.label_play.grid(row=0, column=2, padx=1, pady=(10,0))
        
        #self.prev_label = tk.Label(self.central_frame, text="PREV", fg="#EDE8E6", font=("Terminal", 8), bg='#3A3535')
        #self.prev_label.grid(row=2, columnspan=3, padx=(0,30), pady=(5, 0))
        #self.next_label = tk.Label(self.central_frame, text="NEXT", fg="#EDE8E6",font=("Terminal", 8), bg='#3A3535')
        #self.next_label.grid(row=2, columnspan=3, padx=(60,0), pady=(5, 0))
        
        # Define Control Images
        self.play_btn_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/play.png').resize((80, 23)))       
        self.pause_btn_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/pause.png').resize((40,23)))
        self.stop_btn_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/stop.png').resize((40,23)))
        self.previous_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/prev.png').resize((48,9)))
        self.next_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/next.png').resize((48,9)))
        self.power_light_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/power_light.png').resize((20, 20)))


        self.power_on_label = tk.Label(self.black_frame,  text="POWER", font=("terminal", 6), fg="#E9E4B2", bg='#232121')
        self.power_on_label.grid(row=0, column=0, padx=(250,0), pady=(5,0))
        self.power_label_img = tk.Label(self.black_frame, image=self.power_light_img, bg='#232121')
        self.power_label_img.grid(row=0, column=1,pady=(5,0))
        
        # Control Buttons
        self.pause_button = tk.Button(self.controls_frame, image=self.pause_btn_img, command=self.pause)
        self.pause_button.grid(row=1, column=0, pady=(10,5), padx=(15,4))
        
        self.stop_button = tk.Button(self.controls_frame, image=self.stop_btn_img, command=self.stop)
        self.stop_button.grid(row=1, column=1, pady=(10,5), padx=(0,3)) 
        
        self.play_button = tk.Button(self.controls_frame, image=self.play_btn_img, command=self.play_from_selection)
        self.play_button.grid(row=1, column=2, pady=(10,5), padx=(10,15))

        self.prev_button = tk.Button(self.controls_frame, image=self.previous_img, command=self.play_previous)
        self.prev_button.grid(row=3, columnspan=2, padx=(45,0), pady=(5,10))

        self.next_button = tk.Button(self.controls_frame, image=self.next_img, command=self.play_next)
        self.next_button.grid( row=3, columnspan=3, padx=(80,0), pady=(5, 10))
        
        # Volume label
        self.volume_label_frame = tk.Label(self.right_frame, text='VOLUME', font=("Terminal", 8), bg="#3A3535", fg="green")#fg="#E1B19E"
        self.volume_label_frame.grid(padx=(0), pady=(25,0))
        
        # Volume Labels
        self.volume_label = tk.Label(self.right_frame, text="50", bg='#3A3535', font=("Terminal", 9),fg="#C8C49B")
        self.volume_label.grid(padx=(0), pady=(3))

        # Volume SLider
        self.volume_slider =  ttk.Scale(self.right_frame, from_=1, to=100, orient="horizontal", command=self.set_volume, length=110, style="TScale")
        self.volume_slider.grid(padx=(0))
        self.volume_slider.set(50)



        # Random Button
        self.shuffle_button = tk.Button(self.central_frame, text="RANDOM", font=("Terminal", 8), bg="#BDCCD6", command=self.toggle_shuffle)
        self.shuffle_button.grid(row=1, column=1, padx=(90,0), pady=(20,0))

        # Loop Button
        self.loop_button = tk.Button(self.central_frame, text=" LOOP ", font=("Terminal", 8), bg="#BDCCD6", command=self.toggle_loop)#C2DDAC, C4A98A
        self.loop_button.grid(row=1, column=1, padx=(0,25), pady=(20,0))
        

        
        # Meter Label
        #meter_label = tk.Label(self.right_frame, text="______\n _____\n____\n___\n__\n_\n.", bg='#3C3A3A', fg="#E7D3B0")
        #meter_label.grid(row=0, column=3, padx=(5,40), pady=(10,0))
        
        self.fullscreen_button = tk.Button(self.left_frame, text="VIDEO\nFULL SCREEN", font=("Terminal", 8), command=self.enter_fullscreen_video, bg="#E0E0B6")##F7EAC3
        self.fullscreen_button.grid(padx=(20,0), pady=(10,30))
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen_video())
        
        self.left_vu = VUColumn(self.vu_frame_left, channel_index=0)
        self.right_vu = VUColumn(self.vu_frame_right, channel_index=1)
        
        self.left_vu.grid(padx=(15,0), pady=(15,0))
        self.right_vu.grid(padx=(0,13), pady=(15,0))
        
        self.left_vu_label = tk.Label(self.vu_frame_left, text="LEFT", font=("Terminal", 8), bg="#3A3535", fg="#E9E4B2")
        self.left_vu_label.grid(padx=(12,0), pady=(0,5))

        self.right_vu_label = tk.Label(self.vu_frame_right, text="RIGHT", font=("Terminal", 8), bg="#3A3535", fg="#E9E4B2")
        self.right_vu_label.grid(padx=(0,15), pady=(0,5))

        def update_vumeter():
                
                self.root.after(500, update_vumeter)

        update_vumeter()




        
        
        
        
        
        
        
        
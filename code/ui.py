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
        self.root.geometry("500x357")# 560x470
        self.root.title("DK__9000 MEDI/\ PL/\YER")
        self.root.iconbitmap('media_player/graphics/backgrounds/dodorovsky.ico')
        
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg='#3A3535')
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=0)
        self.main_frame.grid_columnconfigure(4, weight=0)
        self.main_frame.grid_rowconfigure(0, weight=0)
        

        
        # Top Frame for Video and Listbox
        self.top_frame = tk.Frame(self.main_frame, bg="#232121")
        self.top_frame.grid(row=1, column=0, columnspan=5, sticky="nsew")
        
        self.black_frame = tk.Frame(self.top_frame, bg="#232121", width=21, height=21)##232121
        self.black_frame.grid( row=0, pady=0, columnspan=5, sticky="n")
        self.black_frame.grid_columnconfigure(0, weight=0)
        self.black_frame.grid_rowconfigure(0, weight=0)

        self.times_frame = tk.Frame(self.main_frame, bg="black")
        self.times_frame.grid(row=2, columnspan=5, sticky="nsew")
        self.times_frame.grid_columnconfigure(0, weight=1)
        self.times_frame.grid_rowconfigure(1, weight=1)
        
        self.midle_frame = tk.Frame(self.main_frame, bg="#3A3535")
        self.midle_frame.grid(row=3, columnspan=5, sticky="nsew")
        
             
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_rowconfigure(2, weight=1)
        self.top_frame.grid_rowconfigure(3, weight=1)# vídeo    
        self.top_frame.grid_columnconfigure(0, weight=1)
        
        self.listbox = tk.Listbox(self.top_frame, bg="black", fg="#197F0F", width=110, height=12, selectbackground="#6A8785", selectforeground="lime",bd=0, highlightthickness=0, relief="flat")
        self.listbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")      
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)
        
        self.video_frame = tk.Frame(self.top_frame, width=450, height=190, bg="black")# width=450, height=340
        self.video_frame.grid(row=1, column=0, sticky="nsew")
        self.video_frame.drop_target_register(DND_FILES)
        self.video_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.video_frame.grid_forget()
        
        self.style = ttk.Style()
        self.style.theme_use('alt')  # # o 'alt', 'default', 'classic', clam

        # Definimos el estilo personalizado
        self.style.configure('Custom.Horizontal.TScale',
                        troughcolor='black',  # canal del slider
                        background='#232121', borderwidth=0, relief='flat') # fondo del widget (no el thumb)
        self.style.configure('TScale',
                        troughcolor="black",  # canal del slider
                        background='#3A3535', borderwidth=0, relief='flat') 
        self.time_slider = ttk.Scale(self.midle_frame, from_=0, to=100, orient="horizontal", value=0, length=700, style="Custom.Horizontal.TScale")# 664
        self.time_slider.grid(row=2, column=0, padx=0, sticky="nsew")
        
        self.current_time_label = tk.Label(self.times_frame, text="--:--", font=("Terminal", 8), fg="#ADADAD", bg='black')##E9E4B2, #FFFCE8
        self.current_time_label.grid(row=3, column=0, padx=2, sticky="w")
        self.total_time_label = tk.Label(self.times_frame, text="--:--", font=("Terminal", 8), fg="#ADADAD", bg='black')#CAFFFE
        self.total_time_label.grid(row=3, column=5, padx=2)
        
        # Vumeter Frame
        self.vu_frame_left = tk.Frame(self.main_frame, bg="#3A3535")
        self.vu_frame_left.grid_columnconfigure(0, weight=1)
        self.vu_frame_left.grid(row=4, column=0, padx=0, pady=(0), sticky="nsew")
        
        self.vu_frame_right = tk.Frame(self.main_frame, bg="#3A3535")
        self.vu_frame_right.grid_columnconfigure(0, weight=1)
        self.vu_frame_right.grid(row=4, column=4, padx=(0,2), pady=(0), sticky="nsew")
        
        # Left Frame
        self.left_frame = tk.Frame(self.main_frame, bg="#3A3535")
        self.left_frame.grid(pady=10,row=4, column=1, sticky="nswe")
        self.left_frame.grid_columnconfigure(1, weight=1)
        
        # Central Frame
        self.central_frame = tk.Frame(self.main_frame, bg='#3A3535')
        self.central_frame.grid_columnconfigure(0, weight=1)
        self.central_frame.grid(row=4, column=2, sticky="nsew")
        
        # Controls Frame
        self.controls_frame = tk.LabelFrame(self.central_frame, text='CONTROLS->- ', font=("Terminal", 8), bg="#3A3535", fg="green")#fg="#E1B19E",  labelanchor="n",
        self.controls_frame.grid(row=0, column=0, padx=(20,0), pady=7) 

        self.sub_frame_1 = tk.Frame(self.controls_frame, bg="#3A3535")
        self.sub_frame_1.grid()
        self.sub_frame_2 = tk.Frame(self.controls_frame, bg="#3A3535")
        self.sub_frame_2.grid()
        
        
        # Right Frame
        self.right_frame = tk.Frame(self.main_frame, bg='#3A3535')
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid(padx=(8,8),pady=25, row=4, column=3, sticky="nswe")   
        


        # Load button label-Frame
        self.load_label_frame = tk.Label(self.left_frame, text='LOAD_MEDIA', font=("Terminal", 8), bg="#3A3535", fg="green")#fg="#E1B19E"
        self.load_label_frame.grid(padx=(13,0), pady=(5,0), column=1)
        
        #self.mp6_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/mp6.png').resize((40, 23)))
   
        # Load Button
        self.load_button = tk.Button(self.left_frame, bd=1, command=self.load_files, bg="#E9B46F")#bg="#F0C74C"
        self.load_button.grid(padx=(13,0), pady=5, column=1)
        
        # Define Control Images
        self.play_off = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/play_off_b.png').resize((55, 15)))
        self.play_on = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/play_on_b_fluo.png').resize((55, 15)))       
       
        self.pause_off = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/pausa_off_b.png').resize((28,16)))
        self.pause_on = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/pausa_on_b.png').resize((28,16)))

        self.stop_off = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/stop_off_b.png').resize((28,16)))
        self.stop_on = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/stop_on_b.png').resize((28,16)))

        self.previous_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/prev.png').resize((38,7)))
        self.next_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/next.png').resize((38,7)))
        self.hal_on = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/power_light.png').resize((21, 21)))#20,20


        #self.power_on_label = tk.Label(self.black_frame,  text="POWER", font=("terminal", 6), fg="#E9E4B2", bg='#1a1a1a')
        #self.power_on_label.grid(row=0, column=0, padx=(250,0), pady=(3,0))
# Subframe con tamaño exacto para la imagen
# Label con imagen, sin padding ni bordes
        self.hal_label = tk.Label(self.black_frame, image=self.hal_on, width=21, height=21,  bg='#232121')
        self.hal_label.grid(row=0, column=3,pady=(0))
        

        
        self.hal_frames = [ImageTk.PhotoImage(Image.open(f"media_player/graphics/hal_ojo/hal_dim_{i}.png").resize((20,20))) for i in range(0,83)]
        
        # Control Buttons
        self.pause_button = tk.Button(self.sub_frame_1, image=self.pause_off, command=self.pause)
        self.pause_button.grid(row=0, column=0, padx=(7,2), pady=5)
        
        self.stop_button = tk.Button(self.sub_frame_1, image=self.stop_on, command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=1, pady=5) 
        
        self.play_button = tk.Button(self.sub_frame_1, image=self.play_off, command=self.play_from_selection)
        self.play_button.grid(row=0, column=2, padx=9, pady=5)

        self.prev_button = tk.Button(self.sub_frame_2, image=self.previous_img, command=self.play_previous)
        self.prev_button.grid(row=1, column=1, padx=(10,1), pady=5)

        self.next_button = tk.Button(self.sub_frame_2, image=self.next_img, command=self.play_next)
        self.next_button.grid(row=1, column=2, padx=2, pady=5)
        
        
        # Volume Labels
        self.volume_label = tk.Label(self.right_frame, text="50", bg='#3A3535', font=("Terminal", 8),fg="#E9E4B2")#D5FBFB
        self.volume_label.grid()

        # Volume SLider
        self.volume_slider =  ttk.Scale(self.right_frame, from_=0, to=100, orient="horizontal", command=self.set_volume, length=110, style="TScale")
        self.volume_slider.grid(padx=(5,0))
        self.volume_slider.set(50)

        # Volume label
        self.volume_label_frame = tk.Label(self.right_frame, text='[.....VOLUME......]', font=("Terminal", 8), bg="#3A3535", fg="green")#fg="#E1B19E"
        self.volume_label_frame.grid()
        
        self.mute_button = tk.Button(self.right_frame, text="MUTE", font=("Terminal", 8), command=self.toggle_mute, bg="#F4C9A1")
        self.mute_button.grid(pady=5)
        
        self.compact_button = tk.Button(self.left_frame, text="CRT/AMP", font=("Terminal", 8), bg="#959688", command=self.compact)
        self.compact_button.grid(padx=(13,0), column=1)
        

        
        # Random Button
        self.shuffle_button = tk.Button(self.central_frame, text="RANDOM", font=("Terminal", 8), bg="#BDCCD6", command=self.toggle_shuffle)
        self.shuffle_button.grid(row=1,padx=(0, 30), pady=(5,0))

        # Loop Button
        self.loop_button = tk.Button(self.central_frame, text=" LOOP ", font=("Terminal", 8), bg="#BDCCD6", command=self.toggle_loop)#C2DDAC, C4A98A
        self.loop_button.grid(row=1,padx=(80, 0), pady=(5,0))
        

        
        # Meter Label
        #meter_label = tk.Label(self.right_frame, text="______\n _____\n____\n___\n__\n_\n.", bg='#3C3A3A', fg="#E7D3B0")
        #meter_label.grid(row=0, column=3, padx=(5,40), pady=(10,0))
        
        self.fullscreen_button = tk.Button(self.left_frame, text="FULLSCREEN", font=("Terminal", 8), command=self.enter_fullscreen_video, bg="#EBE1AD")##F7EAC3
        self.fullscreen_button.grid(padx=(13,0),pady=(7,30), column=1)
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen_video())
        
        self.mp6 = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/mp6.png').resize((22,10)))
        self.mp6_off = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/mp6_off.png').resize((22,10)))

        
        self.left_vu = VUColumn(self.vu_frame_left, channel_index=0)
        self.right_vu = VUColumn(self.vu_frame_right, channel_index=1)
        
        self.left_vu.grid(padx=(0,6), pady=(0))
        self.right_vu.grid(padx=(5,6), pady=(0))

        
        self.left_vu_label = tk.Label(self.vu_frame_left, text="LEFT", font=("Terminal", 8), bg="#3A3535", fg="#E9E4B2")
        self.left_vu_label.grid(padx=(0,5))
        
        self.mp6_label_left = tk.Label(self.vu_frame_left, image=self.mp6_off, bg="#3A3535")
        self.mp6_label_left.grid(padx=(0,5))

        self.right_vu_label = tk.Label(self.vu_frame_right, text="RIGHT", font=("Terminal", 8), bg="#3A3535", fg="#E9E4B2")
        self.right_vu_label.grid(padx=(0), pady=(0))
        
        self.mp6_label_right = tk.Label(self.vu_frame_right, image=self.mp6_off, bg="#3A3535")
        self.mp6_label_right.grid(padx=(0))
        
        self.breathe_hal()

        def update_vumeter():
                
                self.root.after(500, update_vumeter)


        update_vumeter()
        





        
        
        
        
        
        
        
        
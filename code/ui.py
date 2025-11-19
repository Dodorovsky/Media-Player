

from tkinter import PhotoImage
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import vlc 
import os

from modules import playlist_manager

def setup_ui(self):
        self.root.title("Reproductor con lista")
        self.root.configure(bg="#2C2929")
        self.root.geometry("600x383")
        self.root.resizable(False, False)
        self.root.title("DK_9000 MEDIA PL/\\YER")
        self.root.iconbitmap('media_player/graphics/backgrounds/dodorovsky.ico')
        
        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#2C2B29")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(0, minsize=28)
        for i in range(5):
                self.main_frame.grid_columnconfigure(i, weight=1)
 
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.black_frame = tk.Frame(self.main_frame, bg="#1D1C1B")
        self.black_frame.grid(row=0, column=0, columnspan=5, sticky="nsew")
 
        self.black_frame.grid_columnconfigure(0, weight=1)
        self.black_frame.grid_columnconfigure(2, weight=1)
        self.black_frame.grid_columnconfigure(1, weight=1)
        self.black_frame.grid_rowconfigure(0, minsize=25)

        self.hal_on = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/power_light.png').resize((21, 21)))#20,20

        self.hal_label = tk.Label(self.black_frame, image=self.hal_on, bg='#1D1C1B')
        self.hal_label.grid(row=0, column=1, pady=(3,0), sticky="ns")
        
        # Preload HAL eye frames for breathing animation (sequence of 83 images)
        self.hal_frames = [ImageTk.PhotoImage(Image.open(f"media_player/graphics/hal_ojo/hal_dim_{i}.png").resize((21,21))) for i in range(0,83)]
        
        self.top_frame = tk.Frame(self.main_frame, bg="#2C2929")
        self.top_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")
        self.top_frame.grid_rowconfigure(0, weight=0)
        self.top_frame.grid_rowconfigure(1, weight=1) 
        self.top_frame.grid_rowconfigure(2, weight=0)
        self.top_frame.grid_rowconfigure(3, weight=0)
        self.top_frame.grid_columnconfigure(0, weight=1)
 
        self.times_frame = tk.Frame(self.main_frame, bg="black", width=500)
        self.times_frame.grid(row=3, columnspan=5, sticky="nsew")
        self.times_frame.grid_columnconfigure(0, weight=1)
        self.times_frame.grid_rowconfigure(1, weight=1)
        
        self.midle_frame = tk.Frame(self.main_frame, bg="#2C2929")
        self.midle_frame.grid(row=4, columnspan=5, sticky="nsew")

        self.listbox = tk.Listbox(self.top_frame, bg="black", fg="#27A01C", width=110, height=13, selectbackground="#4B5C5B", selectforeground="lime",bd=0, highlightthickness=0, relief="flat")
        self.listbox.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")      
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)
         
        self.placeholder = tk.Label(self.listbox, text="DRAG_YOUR_FILES_HERE",  fg="#62985C", font=("Monospace", 8), bg="black")
        self.placeholder.place(relx=0.5, rely=0.6, anchor="center")
        
        self.logo_image = ImageTk.PhotoImage(Image.open('media_player/graphics/backgrounds/dodorovsky.png').resize((58, 33)))
        self.radio_image = ImageTk.PhotoImage(Image.open('media_player/graphics/backgrounds/radio.png').resize((80, 47)))

        self.logo_listbox = tk.Label(self.listbox, image=self.logo_image, bg="black")
        self.logo_listbox.place(relx=0.5, rely=0.4, anchor="center")
        
        self.video_frame = tk.Frame(self.top_frame, width=450, height=195, bg="black")
        self.video_frame.grid(row=1, column=0, sticky="nsew")
        self.video_frame.drop_target_register(DND_FILES)
        self.video_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.video_frame.grid_forget()
        
        self.style = ttk.Style()
        self.style.theme_use('alt')  # 'alt', 'default', 'classic', clam


        self.style.configure('Custom.Horizontal.TScale',
                        troughcolor='black',  # slider time 
                        background='#2C2929', borderwidth=0, relief='flat') 
        self.style.configure('TScale',
                        troughcolor="#88682A",  # slider volume 
                        background="#2C2929", borderwidth=0, relief='flat') 
        self.time_slider = ttk.Scale(self.midle_frame, from_=0, to=100, orient="horizontal", value=0, length=640, style="Custom.Horizontal.TScale", command=self.on_slider_move)# 664
        self.time_slider.grid(row=2, column=0, padx=0, sticky="nsew")
        
        self.current_time_label = tk.Label(self.times_frame, text="--:--", font=("Terminal", 8), fg="#ADADAD", bg='black')
        self.current_time_label.grid(row=3, column=0, padx=2, sticky="w")
        self.total_time_label = tk.Label(self.times_frame, text="--:--", font=("Terminal", 8), fg="#ADADAD", bg='black')
        self.total_time_label.grid(row=3, column=5, padx=2)
        
        self.vu_frame_left = tk.Frame(self.main_frame, bg="#2C2929")
        self.vu_frame_left.grid_columnconfigure(0, weight=1)
        self.vu_frame_left.grid(row=5, column=0, padx=15, pady=(0))
        
        self.vu_frame_right = tk.Frame(self.main_frame, bg="#2C2929")
        self.vu_frame_right.grid_columnconfigure(0, weight=1)
        self.vu_frame_right.grid(row=5, column=4, padx=(10), pady=(0))
        
        self.left_frame = tk.Frame(self.main_frame, bg="#2C2929")
        self.left_frame.grid(padx=(15,0),pady=(0,10),row=5, column=1)
        self.left_frame.grid_columnconfigure(1, weight=1)
        
        self.central_frame = tk.Frame(self.main_frame, bg="#2C2929")
        self.central_frame.grid_columnconfigure(0, weight=1)
        self.central_frame.grid(row=5, column=2, sticky="n")
        
        self.controls_frame = tk.LabelFrame(self.central_frame, text='CONTROLS->- ', font=("Terminal", 8), bg="#232121", fg="green")#fg="#E1B19E",  labelanchor="n",
        self.controls_frame.grid(row=0, column=0, padx=(40,0), pady=(7,0)) 

        self.sub_frame_1 = tk.Frame(self.controls_frame, bg="#2C2929")
        self.sub_frame_1.grid()
        self.sub_frame_2 = tk.Frame(self.controls_frame, bg="#2C2929")
        self.sub_frame_2.grid()
        
        self.right_frame = tk.Frame(self.main_frame, bg="#2C2929")
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid(padx=(0), pady=(0), row=5, column=3, sticky="e")   
        
        self.playlist_label = tk.Label(self.left_frame, text = "PLAYLIST", font=("Terminal", 8),bg="#2C2929",fg="green")
        self.playlist_label.grid(padx=0, pady=(13,0))

        self.playlist_button = tk.Menubutton(self.left_frame, relief="groove", bg="#BC853D", fg="black", font=("Monospace", 6))
        self.playlist_button.grid( pady=(5,0))
        
        self.load_line = tk.Label(self.left_frame, text = "__________", font=("Terminal", 3),bg="#2C2929",fg="black")
        self.load_line.grid()
        
        self.load_label_frame = tk.Label(self.left_frame, text=' LOAD_MEDIA', font=("Terminal", 8), bg="#2C2929", fg="green")#fg="#E1B19E"
        self.load_label_frame.grid(pady=(2))
        
        self.load_button = tk.Button(self.left_frame, bd=1, command=self.load_files, bg="#BC853D")#bg="#F0C74C"
        self.load_button.grid(padx=(1,0), pady=(0,10), column=0)
        
        self.play_off = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/play_off_b.png').resize((49, 14)))
        self.play_on = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/play_on_b_fluo.png').resize((49, 14)))       
       
        self.pause_big = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/pause_big.png').resize((49, 14)))
        self.pause_on = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/pausa_on_b.png').resize((28,16)))

        self.stop_off = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/stop_big.png').resize((49, 14)))
        self.stop_on = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/stop_big.png').resize((49, 14)))

        self.previous_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/prev.png').resize((38,7)))
        self.next_img = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/next.png').resize((38,7)))
        
        self.stop_button = tk.Button(self.sub_frame_1, image=self.stop_on, command=self.stop)
        self.stop_button.grid(row=0, column=2, padx=9, pady=5) 
        
        self.play_pause_button = tk.Button(self.sub_frame_1, image=self.play_off, command=self.play_pause)
        self.play_pause_button.grid(row=0, column=1, padx=(10,0), pady=5)

        self.prev_button = tk.Button(self.sub_frame_2, image=self.previous_img, command=self.play_previous)
        self.prev_button.grid(row=1, column=1, padx=(0,2), pady=8)

        self.next_button = tk.Button(self.sub_frame_2, image=self.next_img, command=self.play_next)
        self.next_button.grid(row=1, column=2, padx=2, pady=8)
        
        self.volume_label = tk.Label(self.right_frame, text="90", bg='#2C2929', font=("Terminal", 8),fg="#B2E4E9")#D5FBFB
        self.volume_label.grid(row=0, padx=(7,0), column=0, columnspan=2, sticky="n")

        self.volume_slider =  ttk.Scale(self.right_frame, from_=0, to=100, orient="horizontal", length=110, style="TScale")
        self.volume_slider.grid(row=1, column=0, columnspan=2, padx=(15,0))
        self.volume_slider.set(90)
        self.volume_slider.config( command=self.set_volume)

        self.volume_label_frame = tk.Label(self.right_frame, text='[.....VOLUME......]', font=("Terminal", 8), bg="#2C2929", fg="green")#fg="#E1B19E"
        self.volume_label_frame.grid(row=2, padx=(15,0), column=0, columnspan=2)
        
        self.mute_button = tk.Button(self.right_frame, text="MUTE", font=("Terminal", 6), command=self.toggle_mute, bg="#3E3838", fg="#E0D2D2")
        self.mute_button.grid(row=3, column=0, columnspan=2,padx=(12,0),pady=5)

        self.shuffle_button = tk.Button(self.central_frame, text="RANDOM", font=("Terminal", 6), bg="#3E3838", fg="#E0D2D2", command=self.toggle_shuffle)#BDCCD6
        self.shuffle_button.grid(row=1,padx=(0, 15), pady=(0))

        self.loop_button = tk.Button(self.central_frame, text=" LOOP ", font=("Terminal", 6), bg="#3E3838", fg="#E0D2D2", command=self.toggle_loop)#C2DDAC, C4A98A
        self.loop_button.grid(row=1,padx=(90, 0), pady=(5))

        self.misc_label = tk.Label(self.vu_frame_left, text="MISC.",bg="#2C2929", fg="green", font=("Terminal", 6) )
        self.misc_label.grid(sticky="n")

        self.eq_button = tk.Button(self.vu_frame_left, text="EQ", bg="#0B0B0B", fg="#E0D2D2", font=("Terminal", 6), command=self.toggle_eq)
        self.eq_button.grid(padx=(0), pady=(5,0))

        self.compact_button = tk.Button(self.vu_frame_left, text="-/+", font=("Terminal", 7, "bold"), bg="#191818", fg="#E0D2D2", command=self.compact)
        self.compact_button.grid(padx=(0), pady=5)

        self.hotkeys = tk.Button(self.vu_frame_left, text="HOTKEYS", bg="#191818", fg="#E0D2D2", font=("Terminal", 7), command=self.show_hotkeys)
        self.hotkeys.grid(pady=0)

        
        self.fullscreen_button = tk.Button(self.vu_frame_left, text="FULLSCREEN",bg="#0B0B0B", fg="#E0D2D2", font=("Terminal", 7), command=self.enter_fullscreen_video)##F7EAC3, #EBE1AD
        self.fullscreen_button.grid(pady=(5,5))
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen_video())
        
        self.mp6 = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/mp6.png').resize((22,9)))
        self.mp6_off = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/mp6_off.png').resize((22,9)))
        
        self.mp6_label_left = tk.Label(self.vu_frame_left, image=self.mp6_off, bg="#2C2929")
        self.mp6_label_left.grid(padx=(0,5), pady=(0), sticky="s")

        # Dictionary of radio stations (name -> stream URL)
        self.radios = {
        "NTS": "https://stream-relay-geo.ntslive.net/stream",
        "KEXP": "https://kexp.streamguys1.com/kexp160.aac",
        "SOMA FM": "http://ice1.somafm.com/secretagent-128-mp3",
        "CLASSIC FM": "https://media-ssl.musicradio.com/ClassicFM"}
        
        self.radio_buttons = {}
        
        # Dictionary of radio stations (name -> stream URL)
        for i, (name, url) in enumerate(self.radios.items()):
                btn = tk.Button(self.vu_frame_right, text=name,  font=("Terminal", 7), command=lambda n=name: self.play_radio(n), bg="#191818", fg="#E0D2D2")
                btn.grid( row=i+1, padx=5, pady=(0, 5))
                self.radio_buttons[name] = btn

        self.radios_labels = tk.Label(self.vu_frame_right, text="RADIO", bg="#2C2929",fg="green", font=("Terminal", 8))
        self.radios_labels.grid(padx=(0), pady=(8,5), row=0)
        
        self.mp6_label_right = tk.Label(self.vu_frame_right, image=self.mp6_off, bg="#2C2929")
        self.mp6_label_right.grid(padx=(0), pady=(0,5), sticky="s")
        
        self.eq_line = tk.Label(self.main_frame, bg="#2C2929", text="___________________________________________________________________________________________________________________________________")
        self.eq_line.grid(row=6, columnspan=5, pady=(0,10), sticky="n")

        self.eq_light_image = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/eq_light.png').resize((11,11)))
        self.eq_light_on_image = ImageTk.PhotoImage(Image.open('media_player/graphics/buttons_control/eq_light_on.png').resize((11,11)))


        self.eq_frame = tk.Frame(self.main_frame, bg="#CEA6A6")
        self.eq_frame.grid(row=7, columnspan=5)
        
        self.eq_light_frame = tk.Frame(self.main_frame, bg="#2C2929")
        self.eq_light_frame.grid(row=8, columnspan=5, padx=(0,21))
        
        # Equalizer sliders for 5 frequency bands
        frequencies = ["60Hz", "250H", "1kHz", "4kHz", "16kHz"]
        self.eq_sliders = []
        self.eq_light_labels = []

        # Create vertical sliders and corresponding light indicators
        for i, freq in enumerate(frequencies):
                slider = tk.Scale(self.eq_frame, from_=12, to=-12, orient='vertical', label=freq, font=("Courier", 8),
                                length=100, width=12, bg="#2C2929", fg="#E9E4B2", troughcolor="#43362E",
                                highlightthickness=0, command=lambda val, idx=i: self.on_slider_change(val, idx)
)               
                slider.set(0)
                slider.grid(row=0, column=i, padx=0)
                self.eq_sliders.append(slider)
                self.eq_frame.grid_columnconfigure(i, minsize=60)
                
                label = tk.Label(self.eq_light_frame, image=self.eq_light_image, bg="#2C2929")
                label.grid(row=1, column=i, padx=32)
                self.eq_light_labels.append(label)
         
        self.playlist_menu = tk.Menu(self.playlist_button, tearoff=0)
        self.playlist_button.config(menu=self.playlist_menu)

        self.playlist_menu.add_command(label="Load Playlist", command=self.load_current_playlist)
        self.playlist_menu.add_command(label="Add to Playlist", command=self.add_to_existing_playlist)
        self.playlist_menu.add_command(label="Create Playlist", command=self.create_new_playlist)
        
        self.breathe_hal()

        self.start_eq_light_loop()

      
        





        
        
        
        
        
        
        
        
from tkinter import PhotoImage
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import vlc 

def setup_ui(self):
        self.root.title("Reproductor con lista")
        self.root.configure(bg="#82726D")
        self.root.geometry("550x480")
        self.root.title("1979_MODEL  ___  media_player >> by DODOROVSKY")
        self.root.iconbitmap('tkinter cursos/object oriented tkinter/dodorovsky.ico')
        
        
        # Main Frame

        self.main_frame = tk.Frame(self.root, bg='#3C3A3A')
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        #self.root.attributes("-fullscreen", True)
        
        #self.root.attributes("-fullscreen", False)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.main_frame.grid_rowconfigure(0, weight=1)  # vídeo
        self.main_frame.grid_columnconfigure(0, weight=1)

        
        # Top Frame for Video and Listbox
        self.top_frame = tk.Frame(self.main_frame, bg='#3C3A3A')
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        self.top_frame.grid_rowconfigure(1, weight=1)  # vídeo
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(self.top_frame, bg="black", fg="#197F0F", width=110, height=18, selectbackground="#267227", selectforeground="lime")
        self.listbox.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="nsew")      
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind('<<Drop>>', self.on_drop)

        self.video_frame = tk.Frame(self.top_frame, width=662, height=290, bg="pink")
        self.video_frame.grid(row=1, column=0,  sticky="nsew")
        self.video_frame.drop_target_register(DND_FILES)
        self.video_frame.dnd_bind('<<Drop>>', self.on_drop)
        self.video_frame.grid_forget()
        
        # Time slider and labels
        style = ttk.Style()
        style.configure('TScale', background="#82270E" )
        style.theme_use('clam')  # o 'alt', 'default', 'classic', clam
        
        self.time_slider = ttk.Scale(self.top_frame, from_=0, to=100, orient="horizontal", value=0, length=664, style="TScale")
        self.time_slider.grid(row=2, column=0, padx=20, sticky="nsew")
        
        
        self.current_time_label = tk.Label(self.top_frame, text="--:--", font=("Terminal", 8), fg="#218514", bg='#3C3A3A')
        self.current_time_label.grid(row=3, column=0, padx=(0, 470))# side="left", padx=30, pady=(0,54)
        self.total_time_label = tk.Label(self.top_frame, text="--:--", font=("Terminal", 8), fg="#218514", bg='#3C3A3A')
        self.total_time_label.grid(row=3, column=0, padx=(470, 0))# side="right", padx=30, pady=(0,54)
        
        
        # Left Frame
        self.left_frame = tk.Frame(self.main_frame, bg='#3C3A3A')
        self.left_frame.grid(row=2, column=0, sticky="n")
        
        # Central Frame
        self.central_frame = tk.Frame(self.main_frame, bg='#3C3A3A')
        self.central_frame.grid(row=2, column=1, sticky="n")
        
        # Right Frame
        self.right_frame = tk.Frame(self.main_frame, bg='#3C3A3A')
        self.right_frame.grid(row=2, column=2, sticky="n")
        
        # Load button label-Frame
        self.load_label_frame = tk.LabelFrame(self.left_frame, text='LOAD', font=("Terminal", 8), bg="#3C3A3A", fg="#BC562E")#fg="#E1B19E"
        self.load_label_frame.grid(row=0, column=0, pady=10)
        
        # Volume Slider label-Frame
        self.volume_label_frame = tk.LabelFrame(self.right_frame, text='VOLUME', font=("Terminal", 8), bg="#3C3A3A", fg="#BC562E")#fg="#E1B19E"
        self.volume_label_frame.grid(row=0, column=1)
        
        # Load Button
        self.load_button = tk.Button(self.load_label_frame, command=self.load_files, bg="#F0C74C")
        self.load_button.grid(padx=(12, 0), pady=5)
        
        # Loop Button
        self.loop_button = tk.Button(self.left_frame, text="🔁 Loop", font=("Helvetica", 7), bg="#C2DDAC", command=self.toggle_loop)
        self.loop_button.grid(pady=(5,0))
        
        # Random Button
        self.shuffle_button = tk.Button(self.left_frame, text="🔀 Random", font=("Helvetica", 7), bg="#A7BF94", command=self.toggle_shuffle)
        self.shuffle_button.grid(pady=(5,0))
        
        # Control Labels
        self.label_pause = tk.Label(self.central_frame, fg="#EDE8E6", text="PAUSE", font=("Helvetica", 7), bg='#3C3A3A')
        self.label_pause.grid(row=0, column=0, padx=1)
        self.label_stop = tk.Label(self.central_frame, text="STOP", fg="#EDE8E6",  font=("Helvetica", 7),bg='#3C3A3A')
        self.label_stop.grid(row=0, column=1, padx=(1))
        self.label_play = tk.Label(self.central_frame, text="PLAY", font=("Helvetica", 7), fg="#EDE8E6", bg='#3C3A3A')
        self.label_play.grid(row=0, column=2, padx=1)
        
        self.prev_label = tk.Label(self.central_frame, text="PREV", fg="#EDE8E6", font=("Helvetica", 7), bg='#3C3A3A')
        self.prev_label.grid(row=2, column=1, padx=(1))
        self.next_label = tk.Label(self.central_frame, text="NEXT", fg="#EDE8E6",font=("Helvetica", 7), bg='#3C3A3A')
        self.next_label.grid(row=2, column=2)
        
        # Define Player Control Buttons
        self.play_btn_img = ImageTk.PhotoImage(Image.open('media_player/audio_buttons/play_pl.png').resize((70, 20)))       
        self.pause_btn_img = ImageTk.PhotoImage(Image.open('media_player/audio_buttons/pausa_pl.png').resize((35,20)))
        self.stop_btn_img = ImageTk.PhotoImage(Image.open('media_player/audio_buttons/stop_pl.png').resize((35,20)))
        self.previous_img = ImageTk.PhotoImage(Image.open('media_player/audio_buttons/prev.png').resize((40,8)))
        self.next_img = ImageTk.PhotoImage(Image.open('media_player/audio_buttons/next.png').resize((40,8)))

        
        # Control Buttons
        self.pause_button = tk.Button(self.central_frame, image=self.pause_btn_img, command=self.pause)
        self.pause_button.grid(row=1, column=0, padx=1)
        
        self.stop_button = tk.Button(self.central_frame, image=self.stop_btn_img, command=self.stop)
        self.stop_button.grid(row=1, column=2, padx=1)
        
        self.play_button = tk.Button(self.central_frame, image=self.play_btn_img, command=self.play_from_selection)
        self.play_button.grid(row=1, column=2, padx=1)

        self.prev_button = tk.Button(self.central_frame, image=self.previous_img, command=self.play_previous)
        self.prev_button.grid(row=3, column=1, padx=(4,10))

        self.next_button = tk.Button(self.central_frame, image=self.next_img, command=self.play_next)
        self.next_button.grid(padx=(10, 0), row=3, column=2)
        
        # Volume Labels
        self.volume_label = tk.Label(self.right_frame, text="50", bg='#3C3A3A', fg="#B44113")
        self.volume_label.grid( row=0, column=2, pady=(0,35), sticky="n")

        # Volume SLider
        self.volume_slider =  ttk.Scale(self.volume_label_frame, from_=100, to=1, orient="vertical", command=self.set_volume, length=110, style="TScale")
        self.volume_slider.grid(padx=(15, 0), pady=5, rowspan=2)
        self.volume_slider.set(50)
        
        # Meter Label
        meter_label = tk.Label(self.right_frame, text="______\n _____\n____\n___\n__\n_\n.", bg='#3C3A3A', fg="#A66A02")
        meter_label.grid(row=0, column=2, padx=1, pady=(5, 0))
        

        self.fullscreen_button = tk.Button(self.left_frame, text="Video Full Screen", font=("Helvetica", 7), command=self.enter_fullscreen_video, bg="#9CC27D")
        self.fullscreen_button.grid(row=4, column=0, padx=10, pady=(5, 20))

        self.root.bind("<Escape>", lambda e: self.exit_fullscreen_video())

        
        
        
        
        
        
        
        
        
        
        
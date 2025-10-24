from tkinter import PhotoImage
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import vlc 


def setup_ui(self):
        self.root.title("Reproductor con lista")
        self.root.configure(bg="#82726D")
        self.root.geometry("740x750")
        self.root.title("1979_MODEL  ___  media_player >> by DODOROVSKY")
        self.root.iconbitmap('tkinter cursos/object oriented tkinter/dodorovsky.ico')
        


        #self.video_frame.pack_forget()  # Lo ocultamos por defecto

        self.container_frame = tk.Frame(self.root)
        self.container_frame.pack(fill="both", expand=True)
        


        self.main_frame = tk.Frame(self.container_frame, bg='#3C3A3A')
        self.main_frame.pack(fill="both", expand=True)

        # Listbox Frame
        self.listbox_frame = tk.Frame(self.main_frame, bg="#3C3A3A")
        self.listbox_frame.pack()
        
        self.video_frame = tk.Frame(self.container_frame, width=662, height=290, bg="black")
        self.video_frame.pack(pady=10)
        
        # Frame izquierdo: contiene los 4 frames apilados
        self.left_frame = tk.Frame(self.main_frame, bg="#3C3A3A")
        self.left_frame.pack(side="left", pady=(0,30))

        # Frame derecho: contiene el slider vertical
        self.right_frame = tk.Frame(self.main_frame, bg="#3C3A3A")
        self.right_frame.pack(side="right")
 
        # Volume Label-Frame
        self.volume_label_frame = tk.LabelFrame(self.right_frame, text='Volume', bg='#3C3A3A', fg="#B44113")
        self.volume_label_frame.grid(row=0, column=1, padx=9)    

                # Embebded Video

        
        # Listbox 
        self.listbox = tk.Listbox(self.listbox_frame, width=110, height=18, bg="yellow", fg="green", selectbackground="#267227", selectforeground="lime")
        self.listbox.grid(row=0, column=0, pady=(30,0))    

        #self.video_frame.grid_forget()
        print("Video frame visible:", self.video_frame.winfo_ismapped())

        
        # Slider Volume
        self.volume_label = tk.Label(self.right_frame, text="50", bg='#3C3A3A', fg="#B44113")
        self.volume_label.grid(pady=(0, 130), row=0, column=2, padx=(0,120))

        self.volume_slider =  ttk.Scale(self.volume_label_frame, from_=100, to=1, orient="vertical", command=self.set_volume, length=130, style="TScale")
        self.volume_slider.grid(padx=(18, 0), pady=(2, 4), row=0, column=1)
        self.volume_slider.set(50)
        
        meter_label = tk.Label(self.right_frame, text="______\n _____\n____\n___\n__\n_\n.", bg='#3C3A3A', fg="#EDE8E6")
        meter_label.grid(padx=(0,120),row=0, column=2)
        
        # Time slider and labels
        style = ttk.Style()
        style.configure('TScale', background="#82270E" )
        style.theme_use('clam')  # o 'alt', 'default', 'classic', clam
        
        self.time_slider = ttk.Scale(self.listbox_frame, from_=0, to=100, orient="horizontal", value=0, length=664, style="TScale")
        self.time_slider.grid(row=1, column=0)
        
        
        self.current_time_label = tk.Label(self.listbox_frame, text="00:00", font=("Terminal", 8), fg="#218514", bg='#3C3A3A')
        self.current_time_label.grid(row=2, column=0, padx=(0, 630))# side="left", padx=30, pady=(0,54)
        self.total_time_label = tk.Label(self.listbox_frame, text="00:00", font=("Terminal", 8), fg="#218514", bg='#3C3A3A')
        self.total_time_label.grid(row=2, column=0, padx=(630, 0))# side="right", padx=30, pady=(0,54)
        
        #____________________________-------------------______________________
        
        
        # Define Player Control Buttons
        self.previous_img = PhotoImage(file='Media Payer/audio_buttons/prev.png')
        self.next_img = PhotoImage(file='Media Payer/audio_buttons/next.png')
        self.play_btn_img = PhotoImage(file=r'C:\Users\dodor\OneDrive\Desktop\Media Payer\audio_buttons\play_pl.png')
        self.pause_btn_img = PhotoImage(file='Media Payer/audio_buttons/pausa_pl.png')
        self.stop_btn_img = PhotoImage(file='Media Payer/audio_buttons/stop_pl.png')
       
        # Control Labels Frame
        self.controls_label_frame = tk.Frame(self.left_frame, bg='#3C3A3A')
        self.controls_label_frame.pack()
                
        # Controls Frame
        self.controls_frame = tk.Frame(self.left_frame, bg='#3C3A3A')
        self.controls_frame.pack()
        
        # Prev Next Label frame
        self.prev_next_label_frame = tk.Frame(self.left_frame, bg='#3C3A3A')
        self.prev_next_label_frame.pack(padx=(0,100))
        
        # Prev Next frame
        self.prev_next_frame = tk.Frame(self.left_frame, bg='#3C3A3A')
        self.prev_next_frame.pack(padx=(0, 90))
        
        
        # Labels Button
        self.label_pause = tk.Label(self.controls_label_frame, fg="#EDE8E6", text="PAUSE", font=("Fixedsys", 1), bg='#3C3A3A')
        self.label_pause.grid(row=0, column=0, padx=(210,15))
        self.label_stop = tk.Label(self.controls_label_frame, text="STOP", fg="#EDE8E6",  font=("Helvetica", 9),bg='#3C3A3A')
        self.label_stop.grid(row=0, column=1, padx=(10,15))
        self.label_play = tk.Label(self.controls_label_frame, text="PLAY", font=("Fixedsys", 8), fg="#EDE8E6", bg='#3C3A3A')
        self.label_play.grid(row=0, column=2, padx=58)
        
        self.prev_label = tk.Label(self.prev_next_label_frame, text="PREV", fg="#EDE8E6", font=("Fixedsys", 5), bg='#3C3A3A')
        self.prev_label.grid(row=0, column=1, padx=(290, 80))
        self.next_label = tk.Label(self.prev_next_label_frame, text="NEXT", fg="#EDE8E6",font=("Fixedsys", 5), bg='#3C3A3A')
        self.next_label.grid(row=0, column=2)

        # Control Buttons
        
        self.pause_button = tk.Button(self.controls_frame, image=self.pause_btn_img, command=self.pause)
        self.pause_button.grid(row=0, column=1, padx=(30, 0))
        
        self.stop_button = tk.Button(self.controls_frame, image=self.stop_btn_img, command=self.stop)
        self.stop_button.grid(row=0, column=2, padx=5)
        
        self.play_button = tk.Button(self.controls_frame, image=self.play_btn_img, command=self.play_from_selection)
        self.play_button.grid(row=0, column=3, padx=(20,0))

        self.prev_button = tk.Button(self.prev_next_frame, image=self.previous_img, command=self.play_previous)
        self.prev_button.grid(row=0, column=0, padx=(265, 22))

        self.next_button = tk.Button(self.prev_next_frame, image=self.next_img, command=self.play_next)
        self.next_button.grid(row=0, column=1)
        

        
        # Load button Frame
        self.load_label_frame = tk.LabelFrame(self.controls_frame, text='LOAD', font=("Terminal", 8), bg="#3C3A3A", fg="#BC562E")#fg="#E1B19E"
        self.load_label_frame.grid(row=0, column=0, padx=(100,0))

        # Button load files
        self.load_button = tk.Button(self.load_label_frame, command=self.load_files, bg="#F0C74C")
        self.load_button.grid(padx=(14,0), pady=(2,5))
        
        # Loop Button
        self.loop_button = tk.Button(self.controls_frame, text="🔁 Loop", command=self.toggle_loop)
        self.loop_button.grid(pady=10)
        
        # Suffle Button
        self.shuffle_button = tk.Button(self.controls_frame, text="🔀 Aleatorio", command=self.toggle_shuffle)
        self.shuffle_button.grid(pady=10)

        




        self.player.audio_set_volume(50)  # volumen inicial
        

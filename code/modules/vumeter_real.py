import tkinter as tk
import sounddevice as sd
import numpy as np
import threading

class RealVUMeter(tk.Frame):
    def __init__(self, master, device_id=1, **kwargs):
        super().__init__(master, **kwargs)
        self.device_id = device_id
        self.canvas = tk.Canvas(self, width=60, height=120, bg="#3C3A3A")
        self.canvas.configure(highlightbackground="#3C3A3A")
        self.canvas.grid()

        # Parámetros visuales
        self.num_columns = 2
        self.num_segments = 20
        self.segment_height = 5
        self.spacing = 2
        self.column_spacing = 20


        
        vumeter_width = self.num_columns * self.column_spacing
        x_offset = (70 - vumeter_width) // 2

        # Crear matriz de segmentos
        self.segments = []
        for col in range(self.num_columns):
            column_segments = []
            for seg in range(self.num_segments):
                x1 = x_offset + col * self.column_spacing
                y1 = 100 - (seg * (self.segment_height + self.spacing))
                x2 = x1 + 15
                y2 = y1 + self.segment_height
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")
                column_segments.append(rect)
            self.segments.append(column_segments)

        self.running = True
        threading.Thread(target=self.listen_audio, daemon=True).start()

    def listen_audio(self):
        def get_color_for_segment(index):
            if index < 7:
                return "green"
            elif index < 13:
                return "orange"
            else:
                return "red"

        def callback(indata, frames, time, status):
            
            self.left_volume = np.linalg.norm(indata[:, 0]) * 5 
            self.right_volume = np.linalg.norm(indata[:, 1]) * 5
            for seg_index, rect in enumerate(self.segments[0]):  # columna izquierda
                color = get_color_for_segment(seg_index) if seg_index < int(self.left_volume) else "gray"
                self.canvas.itemconfig(rect, fill=color)

            for seg_index, rect in enumerate(self.segments[1]):  # columna derecha
                color = get_color_for_segment(seg_index) if seg_index < int(self.right_volume) else "gray"
                self.canvas.itemconfig(rect, fill=color)



        with sd.InputStream(device=self.device_id, callback=callback):
            while self.running:
                sd.sleep(100)

    def stop(self):
        self.running = False

import tkinter as tk
import sounddevice as sd
import numpy as np
import threading

class VUColumn(tk.Frame):
    def __init__(self, master, channel_index, device_id=1, **kwargs):
        super().__init__(master, **kwargs)
        self.channel_index = channel_index  # 0 = left, 1 = right
        self.device_id = device_id
        self.canvas = tk.Canvas(self, width=30, height=110, bg="#3A3535")
        self.canvas.configure(highlightbackground="#3A3535")
        self.canvas.grid()

        self.num_segments = 17
        self.segment_height = 5
        self.spacing = 2

        self.segments = []
        for seg in range(self.num_segments):
            x1 = 5
            y1 = 100 - (seg * (self.segment_height + self.spacing))
            x2 = x1 + 20
            y2 = y1 + self.segment_height
            rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#585454")
            self.segments.append(rect)

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
            volume = np.linalg.norm(indata[:, self.channel_index]) * 5
            for seg_index, rect in enumerate(self.segments):
                color = get_color_for_segment(seg_index) if seg_index < int(volume) else "#585454"
                self.canvas.itemconfig(rect, fill=color)

        with sd.InputStream(device=self.device_id, callback=callback):
            while self.running:
                sd.sleep(100)



    def stop(self):
        self.running = False

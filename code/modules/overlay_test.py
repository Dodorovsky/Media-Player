import tkinter as tk
import sounddevice as sd
import numpy as np
import threading

class RealVUMeter(tk.Frame):
    def __init__(self, master, device_id=1, **kwargs):
        super().__init__(master, **kwargs)
        self.device_id = device_id
        self.canvas = tk.Canvas(self, width=90, height=70, bg="#2E2929")
        self.canvas.configure(highlightbackground="orange", highlightthickness=2)


        self.canvas.pack()
        self.bars = [self.canvas.create_rectangle(i*20, 100, i*20+15, 100, fill="green") for i in range(14)]
        self.running = True
        threading.Thread(target=self.listen_audio, daemon=True).start()

    def listen_audio(self):
        def callback(indata, frames, time, status):
            volume = np.linalg.norm(indata) * 10
            for i, bar in enumerate(self.bars):
                height = max(0, min(100, int(volume * (i + 1) / 14)))
                self.canvas.coords(bar, i*20, 100 - height, i*20+15, 100)
        with sd.InputStream(device=self.device_id, callback=callback):
            while self.running:
                sd.sleep(100)

    def stop(self):
        self.running = False

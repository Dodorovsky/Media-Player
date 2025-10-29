import tkinter as tk

class VUMeter:
    def __init__(self, master, num_bars=10, width=200, height=100):
        self.canvas = tk.Canvas(master, width=width, height=height, bg="#111111", highlightthickness=0)
        self.canvas.place(x=10, y=10)  # Ajustá posición según tu layout

        self.bars = []
        self.num_bars = num_bars
        self.bar_width = width // num_bars
        self.max_height = height

        for i in range(num_bars):
            bar = self.canvas.create_rectangle(
                i * self.bar_width,
                self.max_height,
                (i + 1) * self.bar_width - 2,
                self.max_height,
                fill="#00FF00"
            )
            self.bars.append(bar)

    def update(self, level):
        # level: 0–100 (simulado desde volumen)
        active = int((level / 100) * self.num_bars)
        for i, bar in enumerate(self.bars):
            if i < active:
                height = self.max_height - (i * 8)
                self.canvas.coords(bar, i * self.bar_width, height, (i + 1) * self.bar_width - 2, self.max_height)
                self.canvas.itemconfig(bar, fill="#00FF00")
            else:
                self.canvas.coords(bar, i * self.bar_width, self.max_height, (i + 1) * self.bar_width - 2, self.max_height)

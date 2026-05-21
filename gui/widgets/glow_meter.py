import tkinter as tk

class GlowMeter(tk.Frame):
    def __init__(self, parent, label="", width=460, height=20, *args, **kwargs):
        super().__init__(parent, bg="#0b0b0b", *args, **kwargs)
        
        self.columnconfigure(1, weight=1)

        col = 0
        if label:
            self.label = tk.Label(self, text=label, fg="#888888", bg="#0b0b0b", 
                                  font=("Consolas", 9), width=12, anchor="w")
            self.label.grid(row=0, column=0, padx=(12, 8), pady=4, sticky="w")
            col = 1

        self.canvas = tk.Canvas(
            self, 
            width=width, 
            height=height, 
            bg="#111111", 
            highlightthickness=1,
            highlightbackground="#222222"
        )
        self.canvas.grid(row=0, column=col, padx=(4, 12), pady=4, sticky="ew")

        self.bar = self.canvas.create_rectangle(0, 2, 0, height-2, fill="#00ff88", outline="")

    def set_value(self, value: float):
        value = max(0.0, min(1.0, float(value)))

        self.canvas.update_idletasks()
        current_width = self.canvas.winfo_width()
        bar_width = value * current_width

        self.canvas.coords(self.bar, 0, 2, bar_width, self.canvas.winfo_height() - 2)

        # Dynamic color
        if value <= 0.5:
            r = int(255 * (value / 0.5))
            g = 255
        else:
            r = 255
            g = int(255 * (1.0 - ((value - 0.5) / 0.5)))

        color = f"#{r:02x}{g:02x}00"
        self.canvas.itemconfig(self.bar, fill=color)
import customtkinter as ctk

class GlowMeter(ctk.CTkFrame):
    def __init__(self, parent, label="", width=300, height=20, *args, **kwargs):
        super().__init__(parent, fg_color="transparent", *args, **kwargs)
        
        ctk.CTkLabel(self, text=label, font=("Consolas", 12), width=100, anchor="w").grid(row=0, column=0, padx=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(self, width=width, height=height, corner_radius=4)
        self.progress_bar.grid(row=0, column=1, sticky="w")
        self.progress_bar.set(0)

    def set_value(self, value: float):
        self.progress_bar.set(max(0.0, min(1.0, float(value))))
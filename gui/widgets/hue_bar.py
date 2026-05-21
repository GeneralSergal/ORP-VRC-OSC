import customtkinter as ctk
import colorsys

class HueBar(ctk.CTkFrame):
    def __init__(self, parent, label="", width=300, height=20, *args, **kwargs):
        super().__init__(parent, fg_color="transparent", *args, **kwargs)
        
        # Explicit initialization
        self.width = width
        self.height = height
        
        self.grid_columnconfigure(1, weight=0)
        
        if label:
            ctk.CTkLabel(self, text=label, font=("Consolas", 12), width=100, anchor="w").grid(row=0, column=0, padx=(0, 10))
            col = 1
        else:
            col = 0
            
        self.canvas = ctk.CTkCanvas(self, width=width, height=height, bg="#111111", highlightthickness=0)
        self.canvas.grid(row=0, column=col, sticky="w")

        # Delayed drawing to ensure geometry
        self.after(100, self._draw_gradient)
        self.indicator = self.canvas.create_line(0, 0, 0, height, fill="#ffffff", width=3)

    def _draw_gradient(self):
        for x in range(self.width):
            hue = x / self.width
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            self.canvas.create_line(x, 0, x, self.height, fill=color)
        self.canvas.tag_raise(self.indicator)

    def set_value(self, value: float):
        value = max(0.0, min(1.0, float(value)))
        x = int(value * self.width)
        self.canvas.coords(self.indicator, x, 0, x, self.height)
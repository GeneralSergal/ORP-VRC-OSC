import tkinter as tk
import colorsys

class HueBar(tk.Frame):
    def __init__(self, parent, width=480, height=24, bg="#111111", border="#222222"):
        super().__init__(parent, bg=bg)

        self.width = width
        self.height = height

        self.canvas = tk.Canvas(
            self,
            width=self.width,
            height=self.height,
            bg=bg,
            highlightthickness=1,
            highlightbackground=border,
            bd=0
        )
        self.canvas.pack(fill="x", expand=True, padx=2, pady=2)

        self._draw_gradient()

        # White indicator line
        self.indicator = self.canvas.create_line(
            0, 0, 0, self.height,
            fill="#ffffff", width=3
        )

    def _draw_gradient(self):
        """Draw smooth HSV rainbow gradient"""
        for x in range(self.width):
            hue = x / self.width
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            
            color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            
            self.canvas.create_line(x, 0, x, self.height, fill=color)

    def set_value(self, value: float):
        """Move the indicator to the correct position"""
        try:
            value = float(value)
        except (ValueError, TypeError):
            value = 0.0

        value = max(0.0, min(1.0, value))
        x = int(value * self.width)

        self.canvas.coords(self.indicator, x, 0, x, self.height)


if __name__ == "__main__":
    # Quick test
    root = tk.Tk()
    root.configure(bg="#0b0b0b")
    
    bar = HueBar(root, width=480, height=26)
    bar.pack(padx=20, pady=20)
    
    bar.set_value(0.65)  # Test position
    
    root.mainloop()
import tkinter as tk
from tkinter import ttk
import colorsys
from modules.state import state, state_lock

class ORPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ORP Dashboard")
        self.root.geometry("520x760")
        self.root.configure(bg="#101010")

        # Main log
        self.log_text = tk.Text(root, height=10, width=80, state='disabled', bg="#111", fg="#0f0")
        self.log_text.pack(padx=10, pady=8, fill="x")

        # Debug frame
        self.debug_frame = ttk.LabelFrame(root, text="Live Avatar State")
        self.debug_frame.pack(fill="x", padx=10, pady=5)

        self.debug_fields = [
            "state", "Earmuffs", "VelocityMagnitude", "Voice",
            "CoreGlow", "SensoryGlow", "GroundGlow", "MainHue", "BreathingOn", "TailWag"
        ]

        self.debug_labels = {}
        for field in self.debug_fields:
            lbl = ttk.Label(self.debug_frame, text=f"{field}: --")
            lbl.pack(anchor="w", padx=6, pady=1)
            self.debug_labels[field] = lbl

        # Shader visualization
        self.visual_frame = ttk.LabelFrame(root, text="Shader Visualization")
        self.visual_frame.pack(fill="x", padx=10, pady=5)

        # MainHue rainbow bar
        tk.Label(self.visual_frame, text="MainHue").pack(anchor="w")
        self.hue_canvas = tk.Canvas(self.visual_frame, width=420, height=24, bg="#222")
        self.hue_canvas.pack(pady=4, padx=4)
        self.hue_bar = self.hue_canvas.create_rectangle(0,0,420,24, fill="#f00")

        # Glow meters
        self.glow_meters = {}
        for glow in ["CoreGlow", "SensoryGlow", "GroundGlow"]:
            tk.Label(self.visual_frame, text=glow).pack(anchor="w")
            canvas = tk.Canvas(self.visual_frame, width=420, height=22, bg="#222")
            canvas.pack(pady=3, padx=4)
            bar = canvas.create_rectangle(0,0,0,22, fill="#0f0")
            self.glow_meters[glow] = (canvas, bar)

        self._update_loop()

    def push_log(self, msg):
        self.log_text.configure(state='normal')
        self.log_text.insert('end', f"{msg}\n")
        self.log_text.see('end')
        self.log_text.configure(state='disabled')

    def _update_loop(self):
        with state_lock:
            # Update debug labels
            for key, lbl in self.debug_labels.items():
                value = state.get(key, "--")
                if isinstance(value, float):
                    lbl.config(text=f"{key}: {value:.3f}")
                else:
                    lbl.config(text=f"{key}: {value}")

            # Update MainHue bar
            hue = state.get("MainHue", 0.65)
            self.hue_canvas.itemconfig(self.hue_bar, fill=self.hue_to_rgb(hue))

            # Update glow meters
            for glow, (canvas, bar) in self.glow_meters.items():
                value = state.get(glow, 0.0)
                value = max(0.0, min(1.0, value))
                canvas.coords(bar, 0, 0, value*420, 22)
                canvas.itemconfig(bar, fill=self.glow_color(value))

        self.root.after(33, self._update_loop)  # ~30Hz

    def hue_to_rgb(self, h):
        r,g,b = colorsys.hsv_to_rgb(h%1.0,1.0,1.0)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    def glow_color(self, value):
        if value <= 0.5:
            r = int((value/0.5)*255); g=255
        else:
            r=255; g=int((1-(value-0.5)/0.5)*255)
        b=0
        return f"#{r:02x}{g:02x}{b:02x}"
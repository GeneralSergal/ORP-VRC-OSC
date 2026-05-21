import tkinter as tk
from modules.state import state, state_lock
from gui.widgets.hue_bar import HueBar
from gui.widgets.glow_meter import GlowMeter

class DashboardTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#0b0b0b")
        self.accent = "#00ff99"

        # --- LOG PANEL ---
        self.log_text = tk.Text(self.frame, height=8, bg="#050505", fg=self.accent, 
                                font=("Consolas", 9), relief="flat")
        self.log_text.pack(fill="x", padx=10, pady=5)

        # --- LIVE STATE PANEL ---
        self.state_frame = tk.LabelFrame(self.frame, text="Live Avatar State", bg="#0b0b0b", 
                                         fg="#aaaaaa", font=("Consolas", 10))
        self.state_frame.pack(fill="x", padx=10, pady=5)
        self.state_frame.columnconfigure(0, weight=1)

        self.debug_fields = ["Voice", "MainHue", "CoreGlow", "SensoryGlow", 
                             "GroundGlow", "BreathingOn", "TailWag", "VelocityMagnitude"]
        self.debug_labels = {}
        for i, field in enumerate(self.debug_fields):
            lbl = tk.Label(self.state_frame, text=f"{field}: --", fg=self.accent, 
                           bg="#0b0b0b", font=("Consolas", 9), anchor="w")
            lbl.grid(row=i, column=0, padx=10, pady=1, sticky="w")
            self.debug_labels[field] = lbl

        # --- SHADER VISUALIZATION ---
        self.shader_frame = tk.LabelFrame(self.frame, text="Shader Visualization", bg="#0b0b0b", 
                                          fg="#aaaaaa", font=("Consolas", 10))
        self.shader_frame.pack(fill="x", padx=10, pady=5)
        self.shader_frame.columnconfigure(1, weight=1)

        tk.Label(self.shader_frame, text="MainHue", fg="#888888", bg="#0b0b0b", font=("Consolas", 9)).grid(row=0, column=0, padx=6, pady=5, sticky="w")
        self.hue_bar = HueBar(self.shader_frame, width=400, height=20)
        self.hue_bar.grid(row=0, column=1, padx=6, pady=5, sticky="ew")

        self.glow_meters = {}
        for i, glow_name in enumerate(["CoreGlow", "SensoryGlow", "GroundGlow"]):
            meter = GlowMeter(self.shader_frame, label=glow_name, width=400, height=18)
            meter.grid(row=i+1, column=0, columnspan=2, padx=6, pady=2, sticky="ew")
            self.glow_meters[glow_name] = meter

    def push_log(self, message):
        """Method to append messages to the log text widget."""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def update(self):
        with state_lock: snapshot = state.copy()
        for field, label in self.debug_labels.items():
            val = snapshot.get(field, "--")
            label.config(text=f"{field}: {val:.3f}" if isinstance(val, float) else f"{field}: {val}")
        
        self.hue_bar.set_value(snapshot.get("MainHue", 0.0))
        for name, meter in self.glow_meters.items():
            meter.set_value(snapshot.get(name, 0.0))
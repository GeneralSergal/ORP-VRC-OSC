import tkinter as tk
from modules.state import state, state_lock
from gui.widgets.hue_bar import HueBar
from gui.widgets.glow_meter import GlowMeter

class DashboardTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#0b0b0b")
        self.accent = "#00ff99"

        # LOG
        self.log_text = tk.Text(self.frame, height=8, bg="#050505", fg=self.accent, 
                                font=("Consolas", 9), relief="flat")
        self.log_text.pack(fill="x", padx=10, pady=5)

        # LIVE STATE
        self.state_frame = tk.LabelFrame(self.frame, text="Live Avatar State", bg="#0b0b0b", 
                                         fg="#aaaaaa", font=("Consolas", 10))
        self.state_frame.pack(fill="x", padx=10, pady=5)

        self.debug_fields = ["Voice", "MainHue", "CoreGlow", "SensoryGlow", 
                             "GroundGlow", "BreathingOn", "TailWag", "VelocityMagnitude"]
        self.debug_labels = {}
        for i, field in enumerate(self.debug_fields):
            lbl = tk.Label(self.state_frame, text=f"{field}: --", fg=self.accent, 
                           bg="#0b0b0b", font=("Consolas", 9), anchor="w")
            lbl.grid(row=i, column=0, padx=12, pady=2, sticky="w")
            self.debug_labels[field] = lbl

        # ==================== SHADER VISUALIZATION ====================
        self.shader_frame = tk.LabelFrame(self.frame, text="Shader Visualization", 
                                          bg="#0b0b0b", fg="#aaaaaa", font=("Consolas", 10))
        self.shader_frame.pack(fill="x", padx=10, pady=8)

        container = tk.Frame(self.shader_frame, bg="#0b0b0b")
        container.pack(padx=15, pady=10)

        BAR_WIDTH = 460

        # MainHue
        tk.Label(container, text="MainHue", fg="#888888", bg="#0b0b0b", 
                 font=("Consolas", 9)).grid(row=0, column=0, padx=(0,12), pady=6, sticky="w")
        self.hue_bar = HueBar(container, width=BAR_WIDTH, height=24)
        self.hue_bar.grid(row=0, column=1, pady=6)

        # Glow Meters
        self.glow_meters = {}
        for i, glow_name in enumerate(["CoreGlow", "SensoryGlow", "GroundGlow"]):
            tk.Label(container, text=glow_name, fg="#888888", bg="#0b0b0b", 
                     font=("Consolas", 9)).grid(row=i+1, column=0, padx=(0,12), pady=6, sticky="w")
            
            # Use GlowMeter WITHOUT drawing extra label
            meter = GlowMeter(container, label="", width=BAR_WIDTH, height=20)
            meter.grid(row=i+1, column=1, pady=6)
            self.glow_meters[glow_name] = meter

    def push_log(self, message):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def update(self):
        with state_lock: 
            snapshot = state.copy()
        
        for field, label in self.debug_labels.items():
            val = snapshot.get(field, "--")
            label.config(text=f"{field}: {val:.3f}" if isinstance(val, float) else f"{field}: {val}")
        
        self.hue_bar.set_value(snapshot.get("MainHue", 0.0))
        
        for name, meter in self.glow_meters.items():
            meter.set_value(snapshot.get(name, 0.0))
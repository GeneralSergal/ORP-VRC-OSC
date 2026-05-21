import customtkinter as ctk
import os
import datetime
from modules.state import state, state_lock
from gui.widgets.hue_bar import HueBar
from gui.widgets.glow_meter import GlowMeter

class DashboardTab:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.log_file = os.path.join(os.path.dirname(__file__), "../../logs/runtime.log")

        # UI Initialization
        self._setup_log_card()
        self._setup_state_card()
        self._setup_shader_card()
        
        self._last_state = {}

    def _setup_log_card(self):
        self.log_text = ctk.CTkTextbox(self.frame, height=150, font=("Consolas", 12))
        self.log_text.pack(fill="x", padx=20, pady=(20, 10))
        self._load_log_history()

    def _setup_state_card(self):
        self.state_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        self.state_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.state_frame, text="Live Avatar State", font=("Segoe UI", 16, "bold")).pack(pady=(10, 5))
        
        self.debug_labels = {}
        fields = ["Voice", "MainHue", "CoreGlow", "SensoryGlow", "GroundGlow", 
                  "BreathingOn", "TailWag", "VelocityMagnitude"]
        
        container = ctk.CTkFrame(self.state_frame, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        for field in fields:
            lbl = ctk.CTkLabel(container, text=f"{field}: --", anchor="w", font=("Segoe UI", 11))
            lbl.pack(fill="x", pady=1)
            self.debug_labels[field] = lbl

    def _setup_shader_card(self):
        self.shader_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        self.shader_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.shader_frame, text="Shader Visualization", font=("Segoe UI", 16, "bold")).pack(pady=(10, 10))

        self.visual_meters = {
            "MainHue": HueBar(self.shader_frame, label="MainHue", width=300, height=20),
            "CoreGlow": GlowMeter(self.shader_frame, label="CoreGlow", width=300, height=20),
            "SensoryGlow": GlowMeter(self.shader_frame, label="SensoryGlow", width=300, height=20),
            "GroundGlow": GlowMeter(self.shader_frame, label="GroundGlow", width=300, height=20)
        }
        
        for widget in self.visual_meters.values():
            widget.pack(pady=5, padx=20, anchor="center")

    def _load_log_history(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    for line in f.readlines()[-20:]:
                        self.push_log(line.strip())
            except Exception as e:
                self.push_log(f"System: Could not load logs: {e}")

    def push_log(self, message: str):
        if not message.strip().startswith('['):
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            message = f"[{timestamp}] {message}"
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def update(self):
        with state_lock: snapshot = state.copy()
        
        for field, label in self.debug_labels.items():
            val = snapshot.get(field, "--")
            if val != self._last_state.get(field):
                txt = f"{field}: {val:.3f}" if isinstance(val, (float, int)) else f"{field}: {val}"
                label.configure(text=txt)
        
        for name, widget in self.visual_meters.items():
            val = snapshot.get(name, 0.0)
            if val != self._last_state.get(name):
                widget.set_value(val)
        
        self._last_state = snapshot
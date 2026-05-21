# =========================================================
# gui/tabs/stt_tab.py
# =========================================================

import customtkinter as ctk
import sounddevice as sd
import json
import os
from modules.state import state, state_lock

class STTTab:
    def __init__(self, parent, main_gui, llm_bridge=None):
        self.main_gui = main_gui
        self.config_path = os.path.join(os.path.dirname(__file__), "../../config/stt.json")
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True)
        
        self._load_config()
        self._build_ui()
        self.refresh_devices()

    def _load_config(self):
        self.config = {"enabled": True, "device_index": 0}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    self.config = json.load(f)
            except: pass
        
        # Sync initial state to global state
        with state_lock:
            state["stt_enabled"] = self.config.get("enabled", True)

    def _save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def _build_ui(self):
        ctk.CTkLabel(self.frame, text="🎙️ ORP STT ENGINE", font=("Segoe UI", 24, "bold")).pack(pady=(15, 10))
        
        settings = ctk.CTkFrame(self.frame, corner_radius=10)
        settings.pack(fill="x", padx=20, pady=10)

        self.stt_enabled = ctk.BooleanVar(value=self.config.get("enabled", True))
        ctk.CTkSwitch(
            settings, 
            text="Enable Microphone Listening", 
            variable=self.stt_enabled, 
            command=self.toggle_stt
        ).pack(anchor="w", padx=15, pady=15)

        ctk.CTkLabel(settings, text="Input Device:").pack(anchor="w", padx=15)
        self.device_menu = ctk.CTkOptionMenu(settings, values=["Loading..."], command=self.select_device)
        self.device_menu.pack(fill="x", padx=15, pady=(5, 15))

        self.log_text = ctk.CTkTextbox(self.frame, height=200, font=("Consolas", 13))
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def refresh_devices(self):
        # Only list devices that support input
        try:
            names = [f"{i}: {d['name']}" for i, d in enumerate(sd.query_devices()) if d["max_input_channels"] > 0]
            self.device_menu.configure(values=names)
            if names: self.device_menu.set(names[self.config.get("device_index", 0)])
        except: self.device_menu.configure(values=["No devices found"])

    def select_device(self, selected):
        try:
            idx = int(selected.split(":")[0])
            self.config["device_index"] = idx
            self._save_config()
            self.push_log(f"[STT] Input set to {selected}")
        except: pass

    def toggle_stt(self):
        enabled = self.stt_enabled.get()
        self.config["enabled"] = enabled
        self._save_config()
        
        # Update shared state immediately
        with state_lock:
            state["stt_enabled"] = enabled
            
        self.push_log(f"[STT] Active = {enabled}")

    def push_log(self, text):
        self.log_text.insert("end", f"{text}\n")
        self.log_text.see("end")

    def update(self):
        # This is called by the ORPGUI update loop
        pass
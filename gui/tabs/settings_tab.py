import customtkinter as ctk
import json
import os

class SettingsTab(ctk.CTkFrame):
    def __init__(self, parent, gui_instance):
        super().__init__(parent, fg_color="transparent")
        self.gui = gui_instance
        self.config_path = os.path.join(os.path.dirname(__file__), "../../config/config.json")
        
        ctk.CTkLabel(self, text="Application Settings", font=("Segoe UI", 18, "bold")).pack(pady=20)
        
        # UI Scaling Control
        scale_frame = ctk.CTkFrame(self, fg_color="transparent")
        scale_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(scale_frame, text="Interface Scale:").pack(side="left", padx=10)
        
        self.scale_menu = ctk.CTkOptionMenu(
            scale_frame, 
            values=["1.0", "1.25", "1.5", "2.0"], 
            command=self.apply_scaling
        )
        self.scale_menu.set(str(self._load_current_scale()))
        self.scale_menu.pack(side="right", padx=10)

    def _load_current_scale(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f).get("scale", 1.25)
            except: pass
        return 1.25

    def apply_scaling(self, new_scale):
        scale = float(new_scale)
        # Update config
        with open(self.config_path, "w") as f:
            json.dump({"scale": scale}, f)
        
        # Apply scaling globally
        ctk.set_widget_scaling(scale)
        
        # Resize window
        w = int(1280 * scale)
        h = int(920 * scale)
        self.gui.root.geometry(f"{w}x{h}")

    def update(self):
        pass # Settings don't need a live update loop
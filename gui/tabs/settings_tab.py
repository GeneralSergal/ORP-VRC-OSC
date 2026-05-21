# gui/tabs/settings_tab.py
import customtkinter as ctk
import json
import os

class SettingsTab(ctk.CTkFrame):
    def __init__(self, parent, gui_instance):
        super().__init__(parent, fg_color="transparent")
        self.gui = gui_instance
        self.config_path = os.path.join(os.path.dirname(__file__), "../../config/config.json")
        self.feedback_label = None
        
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="⚙️ Application Settings", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=25)

        ctk.CTkLabel(self, text="Appearance Mode", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=50, pady=(10,5))
        self.appearance_var = ctk.StringVar(value=ctk.get_appearance_mode())
        ctk.CTkOptionMenu(self, values=["Dark", "Light", "System"], variable=self.appearance_var).pack(fill="x", padx=50, pady=6)

        ctk.CTkLabel(self, text="Color Theme", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=50, pady=(15,5))
        self.theme_var = ctk.StringVar(value="green")
        ctk.CTkOptionMenu(self, values=["blue", "dark-blue", "green"], variable=self.theme_var).pack(fill="x", padx=50, pady=6)

        ctk.CTkLabel(self, text="UI Scale", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=50, pady=(15,5))
        self.scale_var = ctk.DoubleVar(value=1.25)
        ctk.CTkOptionMenu(self, values=["0.8", "1.0", "1.25", "1.5", "1.75", "2.0"], variable=self.scale_var).pack(fill="x", padx=50, pady=6)

        ctk.CTkButton(
            self,
            text="Apply All Settings",
            command=self.apply_all,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=40)

    def apply_all(self):
        ctk.set_appearance_mode(self.appearance_var.get().lower())
        ctk.set_default_color_theme(self.theme_var.get())
        ctk.set_widget_scaling(self.scale_var.get())

        try:
            with open(self.config_path, "w") as f:
                json.dump({"scale": self.scale_var.get()}, f, indent=2)
        except:
            pass

        if self.feedback_label:
            self.feedback_label.destroy()

        self.feedback_label = ctk.CTkLabel(
            self, 
            text="✅ Settings Applied Successfully!",
            text_color="#00ff99",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.feedback_label.pack(pady=15)

        # Slower fade: ~4 seconds
        self._fade_out(255, 0, 12)   # smaller step = slower fade

    def _fade_out(self, alpha, target, step):
        if self.feedback_label is None:
            return

        if alpha > target:
            # Fade green from full to transparent
            intensity = int(255 * (alpha / 255))
            color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
            try:
                self.feedback_label.configure(text_color=color)
            except:
                pass
            self.after(50, lambda: self._fade_out(alpha - step, target, step))  # 50ms per step
        else:
            if self.feedback_label:
                self.feedback_label.destroy()
                self.feedback_label = None

    def update(self):
        pass
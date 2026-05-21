import customtkinter as ctk
import sounddevice as sd

class TTSTab:
    def __init__(self, parent, main_gui, tts_engine=None):
        self.main_gui = main_gui
        self.tts_engine = tts_engine
        self.devices = []

        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True)

        self._build_ui()
        self.refresh_devices()

    # =========================================================
    # UI
    # =========================================================
    def _build_ui(self):
        ctk.CTkLabel(self.frame, text="🔊 ORP TTS ENGINE", font=("Segoe UI", 24, "bold")).pack(pady=(15, 10))
        
        self.status_label = ctk.CTkLabel(self.frame, text="TTS READY", text_color="#44ff44", font=("Segoe UI", 14, "bold"))
        self.status_label.pack(pady=(0, 15))

        settings = ctk.CTkFrame(self.frame, corner_radius=10)
        settings.pack(fill="x", padx=20, pady=10)

        # Enable/Monitor
        self.tts_enabled = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(settings, text="Enable TTS", variable=self.tts_enabled, command=self.toggle_tts).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.monitor_enabled = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(settings, text="Monitor Through Speakers", variable=self.monitor_enabled, command=self.toggle_monitor).pack(anchor="w", padx=15, pady=(0, 10))

        # Device Select
        ctk.CTkLabel(settings, text="Output Device:").pack(anchor="w", padx=15)
        self.device_menu = ctk.CTkOptionMenu(settings, values=["Loading..."], command=self.select_device)
        self.device_menu.pack(fill="x", padx=15, pady=(5, 10))
        ctk.CTkButton(settings, text="Refresh Devices", command=self.refresh_devices).pack(padx=15, pady=(0, 15))

        # Test Frame
        test_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        test_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(test_frame, text="Test Speech").pack(anchor="w", padx=15, pady=(10, 5))
        self.test_entry = ctk.CTkEntry(test_frame, height=36)
        self.test_entry.pack(fill="x", padx=15, pady=(0, 10))
        ctk.CTkButton(test_frame, text="TEST TTS", command=self.test_tts, height=36).pack(padx=15, pady=(0, 15))

        # Logs
        self.log_text = ctk.CTkTextbox(self.frame, height=260, font=("Consolas", 13))
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    # =========================================================
    # REFRESH DEVICES
    # =========================================================
    def refresh_devices(self):
        try:
            self.devices = []
            names = []
            for idx, dev in enumerate(sd.query_devices()):
                if dev["max_output_channels"] > 0:
                    label = f"{idx}: {dev['name']}"
                    self.devices.append((label, idx))
                    names.append(label)
            if not names: names = ["No Devices"]
            self.device_menu.configure(values=names)
            if names: self.device_menu.set(names[0])
            self.push_log("[TTS] Devices refreshed")
        except Exception as e:
            self.push_log(f"[TTS ERROR] {e}")

    # =========================================================
    # SELECT DEVICE
    # =========================================================
    def select_device(self, selected):
        try:
            for label, idx in self.devices:
                if label == selected:
                    self.tts_engine.output_device = idx
                    self.tts_engine.save_config()
                    self.push_log(f"[TTS] Device set → {label}")
                    break
        except Exception as e:
            self.push_log(f"[TTS ERROR] {e}")

    # =========================================================
    # TOGGLES
    # =========================================================
    def toggle_tts(self):
        self.tts_engine.set_enabled(self.tts_enabled.get())
        self.push_log(f"[TTS] Enabled = {self.tts_enabled.get()}")

    def toggle_monitor(self):
        self.tts_engine.monitor_enabled = self.monitor_enabled.get()
        self.tts_engine.save_config()
        self.push_log(f"[TTS] Monitor = {self.monitor_enabled.get()}")

    # =========================================================
    # TEST
    # =========================================================
    def test_tts(self):
        text = self.test_entry.get().strip()
        if not text: return
        self.push_log(f"[TEST] {text}")
        self.tts_engine.speak(text)

    # =========================================================
    # LOGGING
    # =========================================================
    def push_log(self, text):
        try:
            self.log_text.insert("end", f"{text}\n\n")
            self.log_text.see("end")
        except Exception as e:
            print(f"[TTS TAB] {e}")

    def update(self):
        pass
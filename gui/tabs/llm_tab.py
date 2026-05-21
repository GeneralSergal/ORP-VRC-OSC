# gui/tabs/llm_tab.py
import customtkinter as ctk
import json
import os

class LLMTab:
    def __init__(self, parent, main_gui, llm_bridge=None):
        self.main_gui = main_gui
        self.llm_bridge = llm_bridge

        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill="both", expand=True)

        self._build_ui()

    def _build_ui(self):
        # HEADER
        ctk.CTkLabel(
            self.frame,
            text="🧠 LM Studio Bridge",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 10))

        self.status_label = ctk.CTkLabel(
            self.frame,
            text="Status: Initializing...",
            text_color="#FFAA00",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.pack(pady=(0, 15))

        # Control Buttons
        btn_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="ENABLE LLM", command=self.enable_llm,
            fg_color="#1B3322", hover_color="#2D5A3A", width=160
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame, text="DISABLE LLM", command=self.disable_llm,
            fg_color="#331B1B", hover_color="#5A2D2D", width=160
        ).pack(side="left", padx=10)

        # Configuration
        cfg_frame = ctk.CTkFrame(self.frame, corner_radius=10)
        cfg_frame.pack(fill="x", padx=25, pady=15)

        self.entries = {}

        fields = [
            ("URL:", "base_url"),
            ("Model:", "model"),
            ("Temperature:", "temperature"),
            ("Min Interval:", "min_interval"),
            ("Timeout (s):", "timeout"),
            ("Max Retries:", "max_retries")
        ]

        for label_text, key in fields:
            row = ctk.CTkFrame(cfg_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=6)

            ctk.CTkLabel(row, text=label_text, width=100, anchor="w").pack(side="left")
            entry = ctk.CTkEntry(row, height=32)
            entry.pack(side="right", fill="x", expand=True)
            self.entries[key] = entry

        self._load_values_into_entries()

        # Save Config Button
        ctk.CTkButton(
            self.frame, text="SAVE CONFIG", command=self.save_config,
            fg_color="#444444", hover_color="#666666"
        ).pack(pady=12)

        # Manual Prompt
        ctk.CTkLabel(self.frame, text="Manual Prompt:", font=ctk.CTkFont(size=13, weight="bold")).pack(
            anchor="w", padx=25, pady=(10, 5)
        )

        self.prompt_entry = ctk.CTkEntry(self.frame, height=40)
        self.prompt_entry.pack(fill="x", padx=25, pady=(0, 10))

        ctk.CTkButton(
            self.frame, text="SEND", command=self.send_manual_prompt,
            width=120, height=40
        ).pack(pady=5)

        # Bridge Output
        ctk.CTkLabel(self.frame, text="Bridge Output:", font=ctk.CTkFont(size=13, weight="bold")).pack(
            anchor="w", padx=25, pady=(15, 5)
        )

        self.log_text = ctk.CTkTextbox(self.frame, height=280, font=ctk.CTkFont(family="Consolas", size=13))
        self.log_text.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    def _load_values_into_entries(self):
        if not self.llm_bridge:
            return
        defaults = {
            "base_url": getattr(self.llm_bridge, "base_url", ""),
            "model": getattr(self.llm_bridge, "model", ""),
            "temperature": getattr(self.llm_bridge, "temperature", 0.78),
            "min_interval": getattr(self.llm_bridge, "min_interval", 0.45),
            "timeout": getattr(self.llm_bridge, "timeout", 20.0),
            "max_retries": getattr(self.llm_bridge, "max_retries", 3)
        }
        for key, entry in self.entries.items():
            entry.delete(0, "end")
            entry.insert(0, str(defaults.get(key, "")))

    def save_config(self):
        try:
            cfg_path = os.path.join(os.path.dirname(__file__), "../../config/llm.json")
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            llm_data = data.setdefault("llm", {})
            for key, entry in self.entries.items():
                val = entry.get().strip()
                if key in ["temperature", "min_interval", "timeout"]:
                    llm_data[key] = float(val) if val else getattr(self.llm_bridge, key, 0.78)
                elif key == "max_retries":
                    llm_data[key] = int(val) if val else 3
                else:
                    llm_data[key] = val

            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            if self.llm_bridge:
                self.llm_bridge.load_config()

            self.receive_llm_message("✅ Configuration Saved")
        except Exception as e:
            self.receive_llm_message(f"❌ Save Failed: {e}")

    def enable_llm(self):
        if self.llm_bridge:
            self.llm_bridge.base_url = self.entries["base_url"].get().strip()
            self.llm_bridge.start()

    def disable_llm(self):
        if self.llm_bridge:
            self.llm_bridge.stop()

    def send_manual_prompt(self):
        if self.llm_bridge and (text := self.prompt_entry.get().strip()):
            self.llm_bridge.send_prompt(text)
            self.prompt_entry.delete(0, "end")

    def update_status(self, text, color="#00FF99"):
        self.status_label.configure(text=text, text_color=color)

    def receive_llm_message(self, message):
        try:
            self.log_text.insert("end", f"{message}\n\n")
            self.log_text.see("end")
        except:
            pass

    def update(self):
        if self.llm_bridge:
            if self.llm_bridge.online and self.llm_bridge.enabled:
                self.update_status("🟢 Server ONLINE", "#44FF44")
            elif self.llm_bridge.enabled:
                self.update_status("⚡ Connecting...", "#FFAA00")
            else:
                self.update_status("❌ DISABLED", "#FF4444")
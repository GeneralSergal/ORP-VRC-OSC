import tkinter as tk
import json
import os

class LLMTab:
    def __init__(self, parent, main_gui, llm_bridge=None):
        self.frame = tk.Frame(parent, bg="#0b0b0b")
        self.main_gui = main_gui
        self.llm_bridge = llm_bridge
        self.accent = "#00ff99"
        
        self._build_ui()

    def _build_ui(self):
        tk.Label(self.frame, text="🧠 LM Studio Bridge", bg="#0b0b0b", fg=self.accent, 
                 font=("Consolas", 16, "bold")).pack(pady=12)

        self.status_label = tk.Label(self.frame, text="Status: Initializing...", 
                                     fg="#ffff00", bg="#0b0b0b", font=("Consolas", 11, "bold"))
        self.status_label.pack(pady=8)

        # Buttons
        btn_frame = tk.Frame(self.frame, bg="#0b0b0b")
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="ENABLE LLM", command=self.enable_llm,
                  bg="#003300", fg=self.accent, font=("Consolas", 10, "bold"), width=18).pack(side="left", padx=6)
        tk.Button(btn_frame, text="DISABLE LLM", command=self.disable_llm,
                  bg="#330000", fg="#ff6666", font=("Consolas", 10, "bold"), width=18).pack(side="left", padx=6)

        # Configuration
        cfg = tk.LabelFrame(self.frame, text=" Configuration ", bg="#0b0b0b", fg="#aaaaaa", 
                           font=("Consolas", 10))
        cfg.pack(fill="x", padx=20, pady=12)

        self.entries = {}

        fields = [
            ("URL:", "base_url", "base_url"),
            ("Model:", "model", "model"),
            ("Temperature:", "temperature", "temperature"),
            ("Min Interval:", "min_interval", "min_interval"),
            ("Timeout (s):", "timeout", "timeout"),
            ("Max Retries:", "max_retries", "max_retries")
        ]

        for label_text, cfg_key, attr in fields:
            f = tk.Frame(cfg, bg="#0b0b0b")
            f.pack(fill="x", padx=12, pady=3)
            tk.Label(f, text=label_text, bg="#0b0b0b", fg="#cccccc", width=16, anchor="w",
                     font=("Consolas", 9)).pack(side="left")
            entry = tk.Entry(f, font=("Consolas", 9), bg="#1a1a1a", fg="#ffffff", relief="flat")
            entry.pack(side="right", fill="x", expand=True, padx=(10, 0))
            self.entries[attr] = entry

        # Load current values
        self._load_values_into_entries()

        tk.Button(self.frame, text="SAVE CONFIG", command=self.save_config,
                  bg="#444444", fg="#ffffff", font=("Consolas", 10, "bold")).pack(pady=8)

        # Manual Prompt
        tk.Label(self.frame, text="Manual Prompt:", bg="#0b0b0b", fg="#ccc", 
                 font=("Consolas", 10)).pack(anchor="w", padx=20, pady=(10,2))
        self.prompt_entry = tk.Entry(self.frame, font=("Consolas", 9), bg="#1a1a1a", fg="#fff")
        self.prompt_entry.pack(fill="x", padx=20, pady=4)

        tk.Button(self.frame, text="SEND PROMPT", command=self.send_manual_prompt,
                  bg=self.accent, fg="#000", font=("Consolas", 10, "bold")).pack(pady=6)

        # Log
        self.log_text = tk.Text(self.frame, height=12, bg="#050505", fg="#00ffaa", 
                               font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, padx=20, pady=8)

    def _load_values_into_entries(self):
        if not self.llm_bridge:
            return
        defaults = {
            "base_url": self.llm_bridge.base_url,
            "model": self.llm_bridge.model,
            "temperature": getattr(self.llm_bridge, "temperature", 0.78),
            "min_interval": getattr(self.llm_bridge, "min_interval", 0.45),
            "timeout": getattr(self.llm_bridge, "timeout", 20.0),
            "max_retries": getattr(self.llm_bridge, "max_retries", 3)
        }
        for attr, entry in self.entries.items():
            val = defaults.get(attr, "")
            entry.delete(0, tk.END)
            entry.insert(0, str(val))

    def save_config(self):
        try:
            cfg_path = os.path.join(os.path.dirname(__file__), "../../config/llm.json")
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            llm_data = data.setdefault("llm", {})

            for attr, entry in self.entries.items():
                val = entry.get().strip()
                if attr in ["temperature", "min_interval", "timeout"]:
                    llm_data[attr] = float(val) if val else getattr(self.llm_bridge, attr, 0.78)
                elif attr == "max_retries":
                    llm_data[attr] = int(val) if val else 3
                else:
                    llm_data[attr] = val

            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            # Update live bridge
            if self.llm_bridge:
                for k, v in llm_data.items():
                    if hasattr(self.llm_bridge, k):
                        setattr(self.llm_bridge, k, v)

            self.receive_llm_message("✅ Configuration Saved Successfully")
        except Exception as e:
            self.receive_llm_message(f"❌ Save Failed: {e}")

    def enable_llm(self):
        if self.llm_bridge:
            # Update from GUI fields
            self.llm_bridge.base_url = self.entries["base_url"].get().strip()
            self.llm_bridge.start()
            self.update_status("Status: ENABLED ✓", "#00ff99")

    def disable_llm(self):
        if self.llm_bridge:
            self.llm_bridge.stop()
            self.update_status("Status: DISABLED", "#ff4444")

    def send_manual_prompt(self):
        if self.llm_bridge and (text := self.prompt_entry.get().strip()):
            self.llm_bridge.send_prompt(text)
            self.prompt_entry.delete(0, tk.END)

    def update_status(self, text, color="#00ff99"):
        self.status_label.config(text=text, fg=color)

    def receive_llm_message(self, message):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def update(self):
        pass
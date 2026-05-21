import tkinter as tk
import requests
import threading
import time
import json
import os

class LLMTab:
    def __init__(self, parent, main_gui, llm_bridge=None):
        self.frame = tk.Frame(parent, bg="#0b0b0b")
        self.main_gui = main_gui
        self.llm_bridge = llm_bridge
        self.accent = "#00ff99"
        
        self._build_ui()
        self._start_status_checker()

    def _load_config_data(self):
        """Helper to safely read from the file."""
        try:
            cfg_path = os.path.join(os.path.dirname(__file__), "../../config/llm.json")
            with open(cfg_path, "r", encoding="utf-8") as f:
                return json.load(f).get("llm", {})
        except:
            return {}

    def _build_ui(self):
        tk.Label(self.frame, text="🧠 LM Studio Bridge", bg="#0b0b0b", fg=self.accent, 
                 font=("Consolas", 16, "bold")).pack(pady=12)

        self.status_label = tk.Label(self.frame, text="Status: Checking...", 
                                     fg="#ffff00", bg="#0b0b0b", font=("Consolas", 11))
        self.status_label.pack(pady=6)

        btnf = tk.Frame(self.frame, bg="#0b0b0b")
        btnf.pack(pady=5)
        tk.Button(btnf, text="ENABLE LLM", command=self.enable_llm, bg="#003300", fg=self.accent, 
                  font=("Consolas", 9, "bold"), width=16).pack(side="left", padx=5)
        tk.Button(btnf, text="DISABLE LLM", command=self.disable_llm, bg="#330000", fg="#ff6666", 
                  font=("Consolas", 9, "bold"), width=16).pack(side="left", padx=5)

        cfg = tk.LabelFrame(self.frame, text=" Configuration ", bg="#0b0b0b", fg="#aaaaaa", font=("Consolas", 10))
        cfg.pack(fill="x", padx=20, pady=10)

        config_data = self._load_config_data()

        def add_input(label, config_key, attr):
            f = tk.Frame(cfg, bg="#0b0b0b")
            f.pack(fill="x", padx=10, pady=2)
            tk.Label(f, text=label, bg="#0b0b0b", fg="#ccc", width=15, anchor="w").pack(side="left")
            entry = tk.Entry(f, font=("Consolas", 9), bg="#1a1a1a", fg="#fff")
            entry.pack(side="right", fill="x", expand=True)
            # Use bridge attribute if available, otherwise fallback to config file
            val = getattr(self.llm_bridge, attr, config_data.get(config_key, ""))
            entry.insert(0, str(val))
            return entry

        self.url_entry = add_input("URL:", "base_url", "base_url")
        self.model_entry = add_input("Model:", "model", "model")
        self.temp_entry = add_input("Temperature:", "temperature", "temperature")
        self.min_int_entry = add_input("Min Interval:", "min_interval", "min_interval")
        self.timeout_entry = add_input("Timeout (s):", "timeout", "timeout")
        self.retries_entry = add_input("Max Retries:", "max_retries", "max_retries")

        tk.Button(self.frame, text="SAVE CONFIG", command=self.save_config,
                  bg="#444444", fg="#ffffff", font=("Consolas", 10, "bold")).pack(pady=5)

        tk.Label(self.frame, text="Manual Prompt:", bg="#0b0b0b", fg="#ccc", font=("Consolas", 10)).pack(anchor="w", padx=20, pady=(5,2))
        self.prompt_entry = tk.Entry(self.frame, font=("Consolas", 9), bg="#1a1a1a", fg="#fff")
        self.prompt_entry.pack(fill="x", padx=20, pady=2)

        tk.Button(self.frame, text="SEND PROMPT", command=self.send_manual_prompt,
                  bg=self.accent, fg="#000", font=("Consolas", 10, "bold")).pack(pady=5)

        self.log_text = tk.Text(self.frame, height=10, bg="#050505", fg="#00ffaa", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, padx=20, pady=5)

    def save_config(self):
        try:
            cfg_path = os.path.join(os.path.dirname(__file__), "../../config/llm.json")
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            def get_val(entry, default, cast_type):
                try: return cast_type(entry.get().strip())
                except: return default

            data["llm"].update({
                "base_url": self.url_entry.get().strip(),
                "model": self.model_entry.get().strip(),
                "temperature": get_val(self.temp_entry, 0.7, float),
                "min_interval": get_val(self.min_int_entry, 0.5, float),
                "timeout": get_val(self.timeout_entry, 20.0, float),
                "max_retries": get_val(self.retries_entry, 3, int)
            })
            
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            
            self.receive_llm_message("✅ Configuration Saved!")
            
            if self.llm_bridge:
                for k, v in data["llm"].items():
                    setattr(self.llm_bridge, k, v)
        except Exception as e:
            self.receive_llm_message(f"❌ Save Failed: {e}")

    def update(self): pass
    def _start_status_checker(self): threading.Thread(target=self._status_checker_loop, daemon=True).start()
    def _status_checker_loop(self):
        while True:
            if self.llm_bridge and getattr(self.llm_bridge, 'enabled', False): self._check_lmstudio_status()
            else: self.update_status("Status: DISABLED", "#ff4444")
            time.sleep(10)

    def _check_lmstudio_status(self):
        if not self.llm_bridge: return
        try:
            root = self.llm_bridge.base_url.rsplit('/v1', 1)[0]
            response = requests.get(f"{root}/v1/models", timeout=3)
            if response.status_code == 200: self.update_status("Status: Server ONLINE ✓", "#00ff99")
            else: self.update_status(f"Status: Error ({response.status_code})", "#ffff00")
        except: self.update_status("Status: Server OFFLINE", "#ff4444")

    def enable_llm(self):
        if self.llm_bridge:
            self.llm_bridge.base_url = self.url_entry.get().strip()
            self.llm_bridge.start()
            self.update_status("Status: ENABLED ✓", "#00ff99")

    def disable_llm(self):
        if self.llm_bridge:
            self.llm_bridge.stop()
            self.update_status("Status: DISABLED", "#ff4444")

    def send_manual_prompt(self):
        if self.llm_bridge and (text := self.prompt_entry.get().strip()): self.llm_bridge.send_prompt(text)

    def update_status(self, text, color="#00ff99"): self.status_label.config(text=text, fg=color)
    def receive_llm_message(self, message):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
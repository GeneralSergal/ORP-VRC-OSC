# =========================================================
# gui/tabs/llm_tab.py
# ORP v2.7
# =========================================================

import customtkinter as ctk
import json
import os

class LLMTab:
    def __init__(self, parent, main_gui, llm_bridge=None):
        self.main_gui = main_gui
        self.llm_bridge = llm_bridge

        self.frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):
        # HEADER
        ctk.CTkLabel(
            self.frame,
            text="🧠 LM Studio Bridge",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(15, 10))

        self.status_label = ctk.CTkLabel(
            self.frame,
            text="Status: Initializing...",
            text_color="#FF4444",
            font=("Segoe UI", 14, "bold")
        )

        self.status_label.pack(pady=(0, 15))

        # BUTTONS
        btn_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="ENABLE LLM",
            command=self.enable_llm,
            fg_color="#1B3322",
            hover_color="#2D5A3A",
            width=140
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_frame,
            text="DISABLE LLM",
            command=self.disable_llm,
            fg_color="#331B1B",
            hover_color="#5A2D2D",
            width=140
        ).pack(side="left", padx=8)

        # CONFIG
        cfg = ctk.CTkFrame(
            self.frame,
            corner_radius=10
        )

        cfg.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.entries = {}

        fields = [
            ("URL:", "base_url"),
            ("Model:", "model"),
            ("Temp:", "temperature"),
            ("Interval:", "min_interval"),
            ("Timeout:", "timeout"),
            ("Retries:", "max_retries")
        ]

        for label_text, attr in fields:
            row = ctk.CTkFrame(
                cfg,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=15,
                pady=4
            )

            ctk.CTkLabel(
                row,
                text=label_text,
                width=80,
                anchor="w"
            ).pack(side="left")

            entry = ctk.CTkEntry(
                row,
                height=30
            )

            entry.pack(
                side="right",
                fill="x",
                expand=True
            )

            self.entries[attr] = entry

        self._load_values_into_entries()

        # SYSTEM PROMPT
        ctk.CTkLabel(
            self.frame,
            text="System Prompt:",
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 4)
        )

        self.system_prompt_box = ctk.CTkTextbox(
            self.frame,
            height=180,
            font=("Consolas", 12)
        )

        self.system_prompt_box.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self._load_prompt_config()

        # SAVE BUTTON
        ctk.CTkButton(
            self.frame,
            text="SAVE CONFIG",
            command=self.save_config,
            fg_color="transparent",
            border_width=1
        ).pack(pady=(5, 15))

        # PROMPT INPUT
        ctk.CTkLabel(
            self.frame,
            text="Manual Prompt:"
        ).pack(
            anchor="w",
            padx=20
        )

        prompt_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        prompt_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 10)
        )

        self.prompt_entry = ctk.CTkEntry(
            prompt_frame,
            height=36
        )

        self.prompt_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        ctk.CTkButton(
            prompt_frame,
            text="SEND",
            width=90,
            height=36,
            command=self.send_manual_prompt
        ).pack(side="right")

        # OUTPUT
        ctk.CTkLabel(
            self.frame,
            text="Bridge Output:"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        self.log_text = ctk.CTkTextbox(
            self.frame,
            height=260,
            font=("Consolas", 13)
        )

        self.log_text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    def _load_values_into_entries(self):
        if not self.llm_bridge:
            return
        defaults = {
            "base_url": self.llm_bridge.base_url,
            "model": self.llm_bridge.model,
            "temperature": self.llm_bridge.temperature,
            "min_interval": self.llm_bridge.min_interval,
            "timeout": self.llm_bridge.timeout,
            "max_retries": self.llm_bridge.max_retries
        }
        for attr, entry in self.entries.items():
            entry.delete(0, "end")
            entry.insert(0, str(defaults.get(attr, "")))

    def _load_prompt_config(self):
        try:
            cfg_path = os.path.join(os.path.dirname(__file__), "../../config/llm_prompts.json")
            if not os.path.exists(cfg_path): return
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            prompt = data.get("core_system", "")
            self.system_prompt_box.delete("1.0", "end")
            self.system_prompt_box.insert("1.0", prompt)
        except Exception as e:
            print(f"[LLM TAB] Prompt load failed: {e}")

    def save_config(self):
        try:
            cfg_path = os.path.join(os.path.dirname(__file__), "../../config/llm.json")
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            llm_data = data.setdefault("llm", {})
            for attr, entry in self.entries.items():
                val = entry.get().strip()
                if attr in ["temperature", "min_interval", "timeout"]:
                    llm_data[attr] = float(val)
                elif attr == "max_retries":
                    llm_data[attr] = int(val)
                else:
                    llm_data[attr] = val
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            
            prompt_cfg = os.path.join(os.path.dirname(__file__), "../../config/llm_prompts.json")
            prompt_text = self.system_prompt_box.get("1.0", "end").strip()
            with open(prompt_cfg, "w", encoding="utf-8") as f:
                json.dump({"core_system": prompt_text}, f, indent=2)
            
            if self.llm_bridge:
                self.llm_bridge.load_config()
            self.receive_llm_message("[SYSTEM] Configuration + prompt saved")
        except Exception as e:
            print(f"[LLM] Save failed: {e}")

    def enable_llm(self):
        if self.llm_bridge:
            self.llm_bridge.base_url = self.entries["base_url"].get().strip()
            self.llm_bridge.start()

    def disable_llm(self):
        if self.llm_bridge:
            self.llm_bridge.stop()

    def send_manual_prompt(self):
        if not self.llm_bridge: return
        text = self.prompt_entry.get().strip()
        if not text: return
        self.llm_bridge.send_prompt(text)
        self.prompt_entry.delete(0, "end")

    def update_status(self, text, color="#00FF99"):
        self.status_label.configure(text=text, text_color=color)

    def receive_llm_message(self, message):
        try:
            self.log_text.insert("end", f"{message}\n\n")
            self.log_text.see("end")
        except Exception as e:
            print(f"[LLM TAB] receive error: {e}")

    # =========================================================
    # UPDATE (Integrated for real-time status polling)
    # =========================================================
    def update(self):
        if self.llm_bridge:
            if self.llm_bridge.online:
                self.update_status("Status: Server ONLINE", color="#44FF44")
            elif self.llm_bridge.running:
                self.update_status("Status: Connecting...", color="#FFAA00")
            else:
                self.update_status("Status: OFFLINE", color="#FF4444")
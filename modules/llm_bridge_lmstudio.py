import json
import requests
import threading
import time
import queue
import os
from urllib.parse import urljoin

from modules.state import state, state_lock
from modules.text_sanitizer import sanitize_for_vrchat, split_chatbox_text

class LMStudioBridge:
    def __init__(self):
        self.base_url = "http://127.0.0.1:1234"
        self.model = "gpt-oss-20b"
        self.timeout = 20.0
        self.temperature = 0.78
        
        self.command_queue = queue.Queue(maxsize=12)
        self.running = False
        self.enabled = False
        self.online = False
        self.gui = None
        self.load_config()

    def load_config(self):
        try:
            cfg_path = os.path.join(os.path.dirname(__file__), "../config/llm.json")
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cfg = data.get("llm", data)
                    root = cfg.get("base_url", self.base_url).strip().rstrip('/')
                    if root.endswith('/v1'):
                        root = root[:-3]
                    self.base_url = f"{root.rstrip('/')}/v1"
                    self.model = cfg.get("model", self.model)
        except Exception as e:
            print(f"[LLM] Config load error: {e}")

    def attach_gui(self, gui):
        self.gui = gui

    def start(self):
        if self.running: return
        self.running = True
        self.enabled = True
        threading.Thread(target=self._processing_loop, daemon=True).start()
        threading.Thread(target=self._health_loop, daemon=True).start()

    def stop(self):
        self.running = False
        self.enabled = False
        self.online = False
        if self.gui: self.gui.update_llm_status("❌ DISABLED", "#ff4444")

    # =====================================================
    # EXPOSED METHODS
    # =====================================================
    def send_prompt(self, user_text: str):
        """Sends a user string to the LLM processing queue."""
        if not self.enabled:
            self.gui_log("[LLM] Bridge is disabled.")
            return
        try:
            self.command_queue.put_nowait(user_text)
            self.gui_log(f"USER → {user_text}")
        except queue.Full:
            self.gui_log("[LLM] Queue full - skipping")

    def gui_log(self, text):
        if self.gui: self.gui.receive_llm_message(text)

    # =====================================================
    # INTERNAL LOGIC
    # =====================================================
    def _health_loop(self):
        while self.running:
            if not self.enabled:
                time.sleep(2)
                continue
            try:
                root = self.base_url.rsplit('/v1', 1)[0]
                response = requests.get(urljoin(root, "v1/models"), timeout=3)
                new_status = (response.status_code == 200)
                if new_status != self.online:
                    self.online = new_status
                    if self.gui: self.gui.update_llm_status("🟢 Server ONLINE" if self.online else "⚠️ OFFLINE", "#44ff44" if self.online else "#ffff00")
            except:
                self.online = False
            time.sleep(10)

    def _processing_loop(self):
        while self.running:
            if self.enabled and self.online and not self.command_queue.empty():
                try:
                    self._call_llm(self.command_queue.get_nowait())
                except Exception as e:
                    print(f"[LLM] Processing error: {e}")
            time.sleep(0.1)

    def _call_llm(self, user_text: str):
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": "You are a playful furry gremlin."}, {"role": "user", "content": user_text}],
            "temperature": self.temperature,
            "max_tokens": 220
        }
        try:
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=self.timeout)
            if response.status_code == 200:
                raw = response.json()["choices"][0]["message"].get("content", "").strip()
                clean = sanitize_for_vrchat(raw)
                self.gui_log(f"AI → {clean}")
                for chunk in split_chatbox_text(clean, limit=140):
                    self._send_to_vrchat_osc(chunk)
                    time.sleep(0.5)
        except Exception as e:
            self.gui_log(f"[LLM] Error: {e}")

    def _send_to_vrchat_osc(self, text):
        print(f"[OSC Chatbox] {text}")
import json
import requests
import threading
import time
import queue
import os

from modules.state import state, state_lock
from modules.text_sanitizer import sanitize_for_vrchat, split_chatbox_text

class LMStudioBridge:
    def __init__(self):
        # Runtime defaults
        self.base_url = "http://127.0.0.1:1234/v1"
        self.model = "gpt-oss-20b"
        self.timeout = 20.0
        self.temperature = 0.78
        self.min_interval = 0.45
        self.max_retries = 3
        
        self.command_queue = queue.Queue(maxsize=12)
        self.running = False
        self.enabled = False
        self.online = False
        self.last_call = 0
        self.gui = None

        self.load_config()

    # =====================================================
    # GUI HOOKS
    # =====================================================
    def attach_gui(self, gui):
        self.gui = gui

    def gui_log(self, text):
        print(text)
        if self.gui:
            try:
                self.gui.receive_llm_message(text)
            except Exception:
                pass

    def update_gui_status(self, text, color="#ffaa00"):
        if self.gui:
            try:
                self.gui.update_llm_status(text, color)
            except Exception as e:
                print(f"[LLM] Bridge GUI update error: {e}")

    # =====================================================
    # CONFIG & STARTUP
    # =====================================================
    def load_config(self):
        try:
            cfg_path = os.path.join(os.path.dirname(__file__), "../config/llm.json")
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cfg = data.get("llm", data)
                    self.base_url = cfg.get("base_url", self.base_url).rstrip('/')
                    self.model = cfg.get("model", self.model)
                    self.timeout = float(cfg.get("timeout", self.timeout))
                    self.temperature = float(cfg.get("temperature", self.temperature))
                    self.max_retries = int(cfg.get("max_retries", self.max_retries))
        except Exception as e:
            print(f"[LLM] Config load failed: {e}")

    def start(self):
        if self.running: return
        self.running = True
        self.enabled = True
        threading.Thread(target=self._processing_loop, daemon=True).start()
        threading.Thread(target=self._health_loop, daemon=True).start()
        self.gui_log(f"🧠 LM Studio Bridge ONLINE → {self.model}")

    def stop(self):
        self.running = False
        self.update_gui_status("❌ DISABLED", "#ff4444")
        self.gui_log("🧠 LM Studio Bridge STOPPED")

    # =====================================================
    # LLM LOGIC & CHATBOX
    # =====================================================
    def _call_llm(self, user_text: str):
        if time.time() - self.last_call < self.min_interval: return
        self.last_call = time.time()

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a playful furry gremlin companion."},
                {"role": "user", "content": user_text}
            ],
            "temperature": self.temperature,
            "max_tokens": 220
        }

        try:
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=self.timeout)
            if response.status_code == 200:
                raw_content = response.json()["choices"][0]["message"].get("content", "").strip()
                
                # Sanitize and handle VRChat chatbox limits
                clean_content = sanitize_for_vrchat(raw_content)
                self.gui_log(f"AI → {clean_content}")
                
                # Split and send to VRChat chatbox
                chunks = split_chatbox_text(clean_content, limit=140)
                for chunk in chunks:
                    self._send_to_vrchat_osc(chunk)
                    time.sleep(0.5) 
                
                self._apply_to_avatar(clean_content)
        except Exception as e:
            self.gui_log(f"[LLM] Error: {e}")

    def _send_to_vrchat_osc(self, text):
        # NOTE: Implement your OSC client send logic here
        # Example: self.osc_client.send_message("/chatbox/input", [text, True])
        print(f"[OSC] Sending to Chatbox: {text}")

    def _apply_to_avatar(self, text: str):
        text_lower = text.lower()
        with state_lock:
            # Add state reaction logic here
            state["MainHue"] = (state.get("MainHue", 0.65) + 0.01) % 1.0

    # =====================================================
    # LOOPS
    # =====================================================
    def _health_loop(self):
        while self.running:
            try:
                response = requests.get(f"{self.base_url}/models", timeout=3)
                self.online = (response.status_code == 200)
                status_text = "🟢 ONLINE" if self.online else "❌ OFFLINE"
                self.update_gui_status(status_text, "#44ff44" if self.online else "#ff4444")
            except: self.online = False
            time.sleep(5)

    def _processing_loop(self):
        while self.running:
            if not self.command_queue.empty() and self.online:
                self._call_llm(self.command_queue.get_nowait())
            time.sleep(0.1)

    def send_prompt(self, user_text: str):
        try:
            self.command_queue.put_nowait(user_text)
            self.gui_log(f"USER → {user_text}")
        except queue.Full:
            self.gui_log("[LLM] Queue full")
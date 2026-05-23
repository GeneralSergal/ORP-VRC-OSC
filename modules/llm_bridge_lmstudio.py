# =========================================================
# ORP LLM BRIDGE - LM STUDIO (v2.9 - SAFE MODE)
# =========================================================

import json
import requests
import threading
import time
import queue
import os

from pythonosc import udp_client
from modules.state import state, state_lock
from modules.text_sanitizer import sanitize_for_vrchat, split_chatbox_text
from modules.tts_engine import TTSEngine
from modules.memory_manager import MemoryManager

class LMStudioBridge:
    def __init__(self):
        self.base_url = "http://127.0.0.1:1234/v1"
        self.model = "gpt-oss-20b"
        self.timeout = 20.0
        self.temperature = 0.78
        self.min_interval = 0.45
        self.system_prompt = "You are the cognitive core of an ORP avatar. Respond ONLY with valid JSON."

        self.osc = udp_client.SimpleUDPClient("127.0.0.1", 9000)
        self.tts = TTSEngine()
        
        # Memory Management
        self.memory = MemoryManager(max_exchanges=5)
        self.context_memory = {"emotion": "NEUTRAL"}
        
        self.command_queue = queue.Queue(maxsize=12)
        self.running = False
        self.enabled = False
        self.online = False
        self.last_call = 0
        self.gui = None

        self.load_config()
        self.load_prompts()

    def attach_gui(self, gui):
        self.gui = gui

    def gui_log(self, text):
        print(text)
        if self.gui:
            try: self.gui.receive_llm_message(text)
            except: 
                try: self.gui.push_log(text)
                except: pass

    def update_gui_status(self, text, color="#ffaa00"):
        if self.gui:
            try: self.gui.update_llm_status(text, color)
            except: pass

    def load_config(self):
        try:
            cfg_path = os.path.join(os.path.dirname(__file__), "../config/llm.json")
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cfg = data.get("llm", data)
                    raw = str(cfg.get("base_url", self.base_url)).strip().rstrip('/')
                    if raw.endswith('/v1'): raw = raw[:-3].rstrip('/')
                    self.base_url = raw + '/v1'
                    self.model = cfg.get("model", self.model)
                    self.temperature = float(cfg.get("temperature", self.temperature))
        except Exception as e:
            print(f"[LLM] Config load failed: {e}")

    def load_prompts(self):
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), "../config/llm_prompts.json")
            if os.path.exists(prompt_path):
                with open(prompt_path, "r", encoding="utf-8") as f:
                    self.system_prompt = json.load(f).get("core_system", self.system_prompt)
        except: pass

    def build_context(self):
        return f"Current emotional state: {self.context_memory['emotion']}\n{self.memory.get_context_string()}"

    def start(self):
        if self.running: return
        self.running = True
        self.enabled = True
        threading.Thread(target=self._processing_loop, daemon=True).start()
        threading.Thread(target=self._health_loop, daemon=True).start()
        self.gui_log(f"🧠 LM Studio Bridge ONLINE → {self.model}")

    def stop(self):
        self.running = False
        self.enabled = False
        self.online = False
        self.update_gui_status("❌ DISABLED", "#ff4444")
        self.gui_log("🧠 LM Studio Bridge STOPPED")

    def _health_loop(self):
        while self.running:
            if not self.enabled:
                time.sleep(1)
                continue
            try:
                base = self.base_url.replace('/v1', '')
                response = requests.get(f"{base}/v1/models", timeout=3)
                self.online = (response.status_code == 200)
                self.update_gui_status("🟢 Server ONLINE" if self.online else "❌ Server OFFLINE", 
                                      "#44ff44" if self.online else "#ff4444")
            except:
                self.online = False
                self.update_gui_status("❌ Server OFFLINE", "#ff4444")
            time.sleep(5)

    def send_prompt(self, user_text: str):
        if not self.enabled: return
        self.command_queue.put_nowait(user_text)
        self.gui_log(f"USER → {user_text}")

    def _processing_loop(self):
        while self.running:
            if not self.command_queue.empty() and self.online and self.enabled:
                try: self._call_llm(self.command_queue.get_nowait())
                except Exception as e: print(f"[LLM] Processing error: {e}")
            time.sleep(0.1)

    def _call_llm(self, user_text: str):
        if time.time() - self.last_call < self.min_interval: return
        self.last_call = time.time()

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "system", "content": self.build_context()},
                {"role": "user", "content": user_text}
            ],
            "temperature": self.temperature,
            "max_tokens": 220
        }

        try:
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=self.timeout)
            raw = response.json()["choices"][0]["message"].get("content", "").strip()

            # AGGRESSIVE SAFE-MODE PARSING
            start, end = raw.find('{'), raw.rfind('}')
            
            if start != -1 and end != -1:
                try:
                    parsed = json.loads(raw[start:end+1])
                    state_name = str(parsed.get("S", "NEUTRAL")).upper()
                    intensity = float(parsed.get("I", 0.5))
                    action = str(parsed.get("A", "standing"))
                    speech = str(parsed.get("T", ""))
                    
                    # Update Memory & State
                    self.memory.add_interaction(user_text, speech)
                    self.context_memory["emotion"] = state_name

                    # UI and Output
                    speech_clean = sanitize_for_vrchat(speech)
                    final_text = f"{state_name} | {intensity:.2f}\n{sanitize_for_vrchat(action)}\n{speech_clean}"
                    self.gui_log(f"AI → {final_text}")

                    if getattr(self.tts, 'enabled', False) and speech_clean.strip():
                        threading.Thread(target=self.tts.speak, args=(speech_clean,), daemon=True).start()

                    for chunk in split_chatbox_text(final_text, limit=220):
                        self._send_to_vrchat_osc(chunk)
                        time.sleep(0.45)

                    self._apply_to_avatar(state_name, intensity)
                except Exception as e:
                    self.gui_log(f"[LLM] Parsing error: {e}")
            else:
                self.gui_log("[LLM] No valid JSON detected, request discarded.")

        except Exception as e:
            self.gui_log(f"[LLM] Request error: {e}")

    def _send_to_vrchat_osc(self, text):
        try: self.osc.send_message("/chatbox/input", [text, True, False])
        except: pass

    def _apply_to_avatar(self, state_name, intensity):
        with state_lock:
            state.update({"Emotion": state_name, "Intensity": intensity})
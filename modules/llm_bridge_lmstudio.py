# modules/llm_bridge_lmstudio.py
import json
import requests
import threading
import time
import queue
from datetime import datetime

try:
    from state import state
except ImportError:
    state = {"excitation": 0.0, "entropy": 0.0, "current_emotion": "NEUTRAL"}

class LMStudioBridge:
    def __init__(self):
        try:
            with open("config/runtime.json", "r") as f:
                cfg = json.load(f)["llm"]
            self.base_url = cfg.get("base_url", "http://192.168.1.100:1234/v1").rstrip('/')
            self.model = cfg.get("model", "gpt-oss-20b")
        except:
            self.base_url = "http://192.168.1.100:1234/v1".rstrip('/')
            self.model = "gpt-oss-20b"

        self.command_queue = queue.Queue()
        self.running = False
        self.session_context = []
        self.last_call = 0

    def start(self):
        self.running = True
        threading.Thread(target=self._processing_loop, daemon=True).start()
        print(f"🧠 LM Studio Bridge ONLINE → {self.model}")

    def send_prompt(self, user_text: str, system_prompt: str = None):
        """Main entry point - call this from voice, chat, etc."""
        self.command_queue.put({
            "user_text": user_text,
            "system_prompt": system_prompt
        })

    def _processing_loop(self):
        while self.running:
            if not self.command_queue.empty():
                self._call_llm(self.command_queue.get_nowait())
            time.sleep(0.1)

    def _call_llm(self, cmd):
        if time.time() - self.last_call < 1.2:  # cooldown
            return
        self.last_call = time.time()

        try:
            messages = [
                {"role": "system", "content": cmd["system_prompt"]},
                {"role": "user", "content": cmd["user_text"]}
            ]

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.85,
                "max_tokens": 350
            }

            resp = requests.post(f"{self.base_url}/chat/completions", 
                               json=payload, timeout=300)

            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"].strip()
                
                if '{' in content:
                    json_part = content[content.find('{'):content.rfind('}') + 1]
                    parsed = json.loads(json_part)
                    self._apply_to_avatar(parsed)

        except:
            pass  # Silent in normal operation

    def _apply_to_avatar(self, data: dict):
        emotion = str(data.get("state", "NEUTRAL")).upper()
        intensity = float(data.get("intensity", 0.5))
        action = str(data.get("action", ""))

        emotion_map = {
            "GREMLIN": (0.85, 0.6), "CHAOS": (0.9, 0.7), "DEMON": (0.88, 0.65),
            "LAURENTIUS": (0.75, 0.4), "EXCITED": (0.82, 0.55),
            "BLACKANGEL": (0.6, 0.3), "CALM": (0.2, 0.1), "NEUTRAL": (0.4, 0.2)
        }

        excitation, entropy = emotion_map.get(emotion, (0.5, 0.3))
        
        state["excitation"] = max(state.get("excitation", 0.0), excitation * intensity)
        state["entropy"] = max(state.get("entropy", 0.0), entropy * intensity)
        state["current_emotion"] = emotion

        print(f"🧠 {datetime.now().strftime('%H:%M:%S')} → {emotion} | Int:{intensity:.2f} | {action[:70]}")
# modules/llm_bridge_lmstudio.py
import json
import requests
import threading
import time
import queue
from datetime import datetime
from modules.health import health
from modules.las import las

class LMStudioBridge:
    def __init__(self):
        self.base_url = "http://192.168.1.100:1234/v1"
        self.model = "gpt-oss-20b"
        self.command_queue = queue.Queue()
        self.running = False
        self.session_context = []
        self.last_call = 0
        self.gui = None

    def attach_gui(self, gui):
        self.gui = gui

    def start(self):
        self.running = True
        threading.Thread(target=self._processing_loop, daemon=True).start()
        print(f"🧠 LM Studio Bridge ONLINE → {self.model}")

    def stop(self):
        self.running = False

    def send_prompt(self, user_text: str, system_prompt: str = None):
        """Public method to send prompt to LLM"""
        if not user_text or len(user_text.strip()) < 2:
            return
        self.command_queue.put({
            "user_text": user_text.strip(),
            "system_prompt": system_prompt
        })

    def _processing_loop(self):
        while self.running:
            if not self.command_queue.empty():
                cmd = self.command_queue.get_nowait()
                self._call_llm(cmd)
            time.sleep(0.08)

    def _call_llm(self, cmd):
        if time.time() - self.last_call < 1.0:
            return
        self.last_call = time.time()

        try:
            messages = []
            if cmd.get("system_prompt"):
                messages.append({"role": "system", "content": cmd["system_prompt"]})
            messages.extend(self.session_context[-6:])
            messages.append({"role": "user", "content": cmd["user_text"]})

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.85,
                "max_tokens": 350
            }

            resp = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=300)

            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"].strip()
                
                # Extract JSON
                if '{' in content:
                    json_part = content[content.find('{'):content.rfind('}') + 1]
                    parsed = json.loads(json_part)
                    self._apply_to_avatar(parsed)
                    
                    # Update context
                    self.session_context.append({"role": "user", "content": cmd["user_text"]})
                    self.session_context.append({"role": "assistant", "content": content})
                    if len(self.session_context) > 12:
                        self.session_context = self.session_context[-12:]
            else:
                print(f"❌ LLM HTTP Error: {resp.status_code}")

        except requests.exceptions.Timeout:
            print("⏰ LLM Timeout - Model is slow")
        except Exception as e:
            print(f"💥 LLM Error: {e}")

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
        
        # Update shared state
        try:
            from state import state
            state["excitation"] = max(state.get("excitation", 0.0), excitation * intensity)
            state["entropy"] = max(state.get("entropy", 0.0), entropy * intensity)
            state["current_emotion"] = emotion
        except:
            pass

        print(f"🧠 {datetime.now().strftime('%H:%M:%S')} → {emotion} | Int:{intensity:.2f} | {action[:70]}")

        # Update health
        health.update(excitation=excitation*intensity, entropy=entropy*intensity)

        # Optional GUI update
        if self.gui and hasattr(self.gui, 'log_llm_response'):
            self.gui.log_llm_response(emotion, intensity, action)


# Global instance
llm_bridge = LMStudioBridge()

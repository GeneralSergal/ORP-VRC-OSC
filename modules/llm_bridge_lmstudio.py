# modules/llm_bridge_lmstudio.py
import json
import requests
import threading
import time
import queue
from datetime import datetime

# Import from existing ORP structure
try:
    from state import state
except ImportError:
    # Fallback if state.py not yet structured
    state = {"excitation": 0.0, "entropy": 0.0, "current_emotion": "NEUTRAL"}

class LMStudioBridge:
    def __init__(self, base_url="http://localhost:1234/v1"):
        self.base_url = base_url
        self.model = "gpt-oss-20b"          # Change if you use different model
        self.command_queue = queue.Queue()
        self.running = False
        self.session_context = []
        self.last_call = 0
        self.min_interval = 0.4             # Safety cooldown

    def start(self):
        self.running = True
        threading.Thread(target=self._processing_loop, daemon=True).start()
        print(f"🔗 LM Studio Bridge ONLINE → {self.base_url} | Model: {self.model}")

    def stop(self):
        self.running = False

    def send_prompt(self, user_text: str, system_prompt: str = None):
        """Send text to LLM and queue for processing"""
        self.command_queue.put({
            "user_text": user_text,
            "system_prompt": system_prompt,
            "timestamp": time.time()
        })

    def _processing_loop(self):
        while self.running:
            if not self.command_queue.empty():
                cmd = self.command_queue.get_nowait()
                self._call_llm(cmd)
            time.sleep(0.08)  # Gentle loop

    def _call_llm(self, cmd):
        if time.time() - self.last_call < self.min_interval:
            return

        self.last_call = time.time()

        try:
            messages = []
            if cmd.get("system_prompt"):
                messages.append({"role": "system", "content": cmd["system_prompt"]})

            # Keep short rolling memory
            messages.extend(self.session_context[-8:])
            messages.append({"role": "user", "content": cmd["user_text"]})

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.78,
                "max_tokens": 400,
                "response_format": {"type": "json_object"}
            }

            resp = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=10)

            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"].strip()

                try:
                    parsed = json.loads(content)
                    self._apply_to_avatar(parsed)
                    
                    # Update context
                    self.session_context.append({"role": "user", "content": cmd["user_text"]})
                    self.session_context.append({"role": "assistant", "content": content})
                    if len(self.session_context) > 12:
                        self.session_context = self.session_context[-12:]
                except json.JSONDecodeError:
                    print("❌ LLM returned non-JSON. Raw:", content[:200])
            else:
                print(f"HTTP Error: {resp.status_code}")

        except Exception as e:
            print(f"LLM Bridge Error: {e}")

    def _apply_to_avatar(self, data: dict):
        """Convert LLM JSON output into ORP physiology signals"""
        emotion = str(data.get("state", "NEUTRAL")).upper()
        intensity = float(data.get("intensity", 0.5))
        action = str(data.get("action", ""))

        excitation = 0.0
        entropy = 0.0

        emotion_map = {
            "LAURENTIUS": (0.78, 0.45),
            "EXCITED": (0.82, 0.5),
            "HYPER": (0.9, 0.6),
            "BLACKANGEL": (0.6, 0.3),
            "TENSION": (0.65, 0.35),
            "DEMON": (0.85, 0.65),
            "CHAOS": (0.88, 0.7),
            "GREMLIN": (0.75, 0.55),
            "CALM": (0.2, 0.1),
            "NEUTRAL": (0.35, 0.2)
        }

        excitation, entropy = emotion_map.get(emotion, (0.4, 0.25))

        # Apply to shared state
        state["excitation"] = max(state.get("excitation", 0.0), excitation * intensity)
        state["entropy"] = max(state.get("entropy", 0.0), entropy * intensity)
        state["current_emotion"] = emotion

        print(f"🧠 {datetime.now().strftime('%H:%M:%S')} | {emotion} | Int: {intensity:.2f} | Act: {action[:50]}")

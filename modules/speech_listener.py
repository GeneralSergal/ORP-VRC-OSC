# =========================================================
# ORP STT LISTENER - INTEGRATED
# =========================================================

import os
import queue
import sounddevice as sd
import json
import threading
from vosk import Model, KaldiRecognizer
from modules.state import state, state_lock

class SpeechListener:
    def __init__(self, llm_bridge):
        self.llm_bridge = llm_bridge
        
        # Path configuration
        model_path = os.path.join(os.path.dirname(__file__), "../stt_models")
        
        print(f"[STT] Loading model from: {model_path}")
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.q = queue.Queue()

    def _audio_callback(self, indata, frames, time, status):
        if status: 
            print(f"[STT] Status: {status}")
        self.q.put(bytes(indata))

    def listen_loop(self):
        print("[HEARING] Microphone active...")
        
        # Open audio stream
        with sd.RawInputStream(samplerate=16000, blocksize=8000, 
                               dtype='int16', channels=1, callback=self._audio_callback):
            while True:
                # Synchronize with global GUI state
                with state_lock:
                    is_enabled = state.get("stt_enabled", True)
                
                # Fetch audio data from queue
                data = self.q.get()
                
                # GATEKEEPER: If STT is disabled in GUI, reset and skip
                if not is_enabled:
                    self.rec.Reset()
                    continue

                # Process audio only if enabled
                if self.rec.AcceptWaveform(data):
                    res = json.loads(self.rec.Result())
                    text = res.get("text", "")
                    
                    # Only proceed if there is substantial text
                    if text and len(text.strip()) > 2:
                        print(f"[HEARING] {text}")
                        # Bridge's internal enabled check provides final safety
                        self.llm_bridge.send_prompt(text)

def start_listening(llm_bridge):
    listener = SpeechListener(llm_bridge)
    threading.Thread(target=listener.listen_loop, daemon=True).start()
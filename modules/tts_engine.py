import os
import json
import tempfile
import threading
import wave
import numpy as np
import sounddevice as sd
import soundfile as sf
from piper import PiperVoice

class TTSEngine:
    def __init__(self):
        self.enabled = True
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Config Path
        self.config_path = os.path.join(self.base_dir, "../config/tts.json")
        self.output_device = None
        self.monitor_enabled = True
        self.sample_rate = 22050

        self.load_config()

        # Model Path
        self.model_path = os.path.join(self.base_dir, "../models/en_US-lessac-medium.onnx")
        self.voice = None

        # Load Voice
        try:
            self.voice = PiperVoice.load(self.model_path)
            print(f"[TTS] Voice loaded → {self.model_path}")
        except Exception as e:
            print(f"[TTS] Voice load failed: {e}")

    # All these methods are now properly indented inside the class
    def load_config(self):
        try:
            if not os.path.exists(self.config_path):
                self.save_config()
                return
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.output_device = data.get("output_device", None)
            self.monitor_enabled = bool(data.get("monitor_enabled", True))
            print(f"[TTS] Config loaded (device={self.output_device})")
        except Exception as e:
            print(f"[TTS] Config load failed: {e}")

    def save_config(self):
        try:
            data = {"output_device": self.output_device, "monitor_enabled": self.monitor_enabled}
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[TTS] Config save failed: {e}")

    def list_devices(self):
        try:
            devices = sd.query_devices()
            for idx, dev in enumerate(devices):
                print(f"[{idx}] {dev['name']}")
            return devices
        except Exception as e:
            print(f"[TTS] Device query failed: {e}")
            return []

    def set_enabled(self, value: bool):
        self.enabled = value
        print(f"[TTS] Enabled = {self.enabled}")

    def speak(self, text: str):
        try:
            if not self.enabled or not self.voice or not text.strip():
                return
            threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
        except Exception as e:
            print(f"[TTS ERROR] {e}")

    def _speak_thread(self, text: str):
        try:
            output_wav = os.path.join(tempfile.gettempdir(), "orp_tts.wav")
            with wave.open(output_wav, "wb") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(self.sample_rate)
                for audio_chunk in self.voice.synthesize(text):
                    wav_file.writeframes(audio_chunk.audio_int16_bytes)

            audio_data, samplerate = sf.read(output_wav, dtype="float32")
            sd.play(audio_data, samplerate, device=self.output_device)
            sd.wait()

            if self.monitor_enabled:
                sd.play(audio_data, samplerate)
                sd.wait()
            print(f"[TTS] SPOKE → {text}")
        except Exception as e:
            print(f"[TTS ERROR] {e}")
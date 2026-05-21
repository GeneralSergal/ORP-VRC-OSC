# ORP-VRC-OSC — Herald of Darkness

**Organic Resonance Physiology** — Advanced OSC middleware for VRChat avatars.

---

## Features

- Deterministic layered physiology system
- Real-time OSC bridge (9005 in / 9000 out)
- Modern GUI Dashboard with live state + shader visualization
- Local LLM integration (LM Studio)
- **Speech-to-Text (STT)** via Vosk
- **Text-to-Speech (TTS)** support
- Timestamped logging

---

## Folder Structure

```bash
ORP-VRC-OSC/
├── main.py
├── launch_osc.bat
├── config/
│   ├── llm.json
│   ├── runtime.json
│   └── hues.json
├── logs/
├── modules/
├── gui/
├── gui/widgets/
├── stt_models/                # Vosk STT models
│   ├── vosk-model-small-en-us-0.15/
│   └── placeholder.md
└── models/                    # TTS models (e.g. Coqui / Piper)
    ├── en_US-lessac-medium.onnx
    ├── en_US-lessac-medium.onnx.json
    └── placeholder.md
```

---

## Dependencies

```bash
pip install python-osc customtkinter requests numpy vosk sounddevice pyaudio
```

---

## Quick Start

1. Install the dependencies above.

2. **STT Model**  
   Download `vosk-model-small-en-us-0.15` and extract it into `stt_models/`.

3. **TTS Model** (optional)  
   Place `en_US-lessac-medium.onnx` + `.json` into the `models/` folder.

4. Configure `config/llm.json`.

5. Run:
   ```bash
   python main.py
   ```

6. Enable LLM in the GUI.

---

**AGPL-3.0**

Chaos-driven avatar middleware.

— GeneralSergal

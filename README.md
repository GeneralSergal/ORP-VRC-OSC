# ORP-VRC-OSC — Herald of Darkness

**Organic Resonance Physiology** — Advanced OSC middleware for VRChat avatars.

A lightweight, modular Python bridge that combines deterministic physiology, real-time OSC routing, shader visualization, and local LLM + STT integration.

---

## Features

- **Real-time Physiology System** — Layered deterministic state synthesis
- **Full OSC Bridge** — Input (9005) / Output (9000) with live debugger
- **Modern GUI Dashboard** — Live state + Shader Visualization (Hue + Glows)
- **Local LLM Integration** — LM Studio (OpenAI compatible)
- **Speech-to-Text Ready** — STT models folder prepared
- **Persistent Logging** — File + GUI with timestamps
- **Manual Control** — LLM starts only when enabled

---

## Current Structure

```
ORP-VRC-OSC/
├── main.py
├── launch_osc.bat
├── config/
│   ├── llm.json
│   ├── runtime.json
│   └── hues.json
├── logs/
├── modules/
│   ├── __init__.py
│   ├── logger.py
│   ├── llm_bridge_lmstudio.py
│   ├── osc_vrc_bridge.py
│   ├── physiology.py
│   ├── state.py
│   ├── vrchat_output.py
│   └── config_loader.py
├── gui/
│   ├── __init__.py
│   ├── orp_gui.py
│   └── tabs/
│       ├── dashboard_tab.py
│       ├── osc_debug_tab.py
│       └── llm_tab.py
├── gui/widgets/
│   ├── hue_bar.py
│   └── glow_meter.py
└── stt_models/          # Speech-to-Text support
```

---

## Quick Start

1. Install dependencies:
   ```bash
   pip install python-osc customtkinter requests
   ```

2. Configure `config/llm.json` with your LM Studio endpoint.

3. Run:
   ```bash
   python main.py
   ```

4. Go to **LLM tab** → Click **ENABLE LLM**

---

## Controls

- **Dashboard**: Live avatar state + Shader Visualization
- **OSC Debug**: Real-time parameter viewer
- **LLM**: Enable/disable bridge, manual prompts, config

---

## License

AGPL-3.0

---

**Made with chaos and love for the gremlins.**

— GeneralSergal

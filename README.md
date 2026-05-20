# ORP-VRC-OSC

**ORP** (Organic Resonance Physiology) is a minimal, layered OSC middleware framework for VRChat avatars.

It uses **deterministic state synthesis** across isolated layers instead of traditional blending and interpolation. This creates more stable, recoverable, and lifelike avatar physiology.

---

## Core Philosophy

- No parameter blending — only controlled synthesis
- Hard domain gating (`0.00-0.50` Observation | `0.51-1.00` Locomotion)
- Voice excitation priority bypass
- Entropy layer for organic jitter
- Strong deterministic recovery
- Instant Safe Mode reset

---

## Features

- Layered deterministic physiology engine
- Real-time voice-reactive behavior
- Organic entropy system
- Live GUI dashboard
- Hot-swappable config system
- Local LLM support (ready for reconnection)
- Clean, minimal runtime

---

## Project Structure

```text
ORP-VRC-OSC/
├── main.py
├── launch_osc.bat
├── README.md
├── LICENSE
│
├── config/
│   ├── hues.json
│   ├── runtime.json
│   ├── llm.json
│   └── llm_prompts.json
│
├── gui/
│   ├── __init__.py
│   └── orp_gui.py
│
└── modules/
    ├── __init__.py
    ├── config_loader.py
    ├── osc_vrc_bridge.py
    ├── physiology.py
    ├── state.py
    ├── vrchat_output.py
    └── llm_bridge_lmstudio.py     # Legacy - disconnected for now
```

---

## Requirements

- Python 3.10+
- `pip install python-osc`

---

## Launch

**Windows (Recommended):**
Double-click `launch_osc.bat`

**Manual:**
```bash
python main.py
```

---

## Default OSC Ports

| Direction         | Port |
|-------------------|------|
| VRChat → ORP      | 9005 |
| ORP → VRChat      | 9000 |

---

## Design Principles

ORP rejects:
- Monolithic code
- Uncontrolled interpolation
- Hidden state drift
- Spaghetti parameter logic

The system is intentionally minimal and readable while remaining highly expandable.

---

## License

**GNU Affero General Public License v3.0 (AGPL-3.0)**

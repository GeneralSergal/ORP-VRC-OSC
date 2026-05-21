# ORP-VRC-OSC

**ORP** (Organic Resonance Physiology) is a minimal, layered OSC middleware framework for VRChat avatars.

It replaces traditional messy parameter blending with **deterministic state synthesis** across cleanly isolated layers. The result is more stable, recoverable, and organic avatar behavior.

---

## Core Philosophy

- **No blending. Only synthesis.**
- Hard domain gating: `0.00–0.50` = Observation | `0.51–1.00` = Locomotion
- Voice excitation has priority bypass
- Entropy layer injects natural jitter
- Strong deterministic recovery + instant Safe Mode

---

## Features

- Layered deterministic physiology engine
- Real-time voice-reactive behavior
- Organic entropy system
- **Advanced GUI Dashboard v2.6** with:
  - Live Avatar State monitoring
  - Shader visualization (CoreGlow, SensoryGlow, etc.)
  - Full OSC Live Debugger
  - Parameter routing table
  - Port rebinding & live log
- Hot-swappable configuration
- Local LLM support ready (bridge available)
- Clean minimal core

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
│   └── orp_gui.py          # v2.6 with full debugger
│
└── modules/
    ├── __init__.py
    ├── config_loader.py
    ├── osc_vrc_bridge.py
    ├── physiology.py
    ├── state.py
    ├── vrchat_output.py
    └── llm_bridge_lmstudio.py   # Legacy - for future reconnection
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

| Direction       | Port |
|-----------------|------|
| VRChat → ORP    | 9005 |
| ORP → VRChat    | 9000 |

---

## Screenshots

**System Dashboard** — Live physiology + shader visualization  
**OSC Live Debugger** — Full parameter routing table + live inspection

---

## Design Principles

- Deterministic over interpolated
- Maximum readability & debuggability
- Minimal core, high expandability
- No hidden middleware

---

## License

**GNU Affero General Public License v3.0 (AGPL-3.0)**

# ORP-VRC-OSC

**ORP** (Organic Resonance Physiology) is a minimal layered OSC middleware for VRChat avatars.

It replaces messy parameter blending with **deterministic state synthesis** across isolated layers merged through a controlled bus. The result is more stable, recoverable, and organic avatar behavior.

---

## Core Philosophy

- **No blending. Only synthesis.**
- Hard domain gating: `0.00–0.50` = Observation domain | `0.51–1.00` = Locomotion domain
- Voice has priority bypass
- Entropy layer adds natural jitter
- Strong deterministic recovery + Safe Mode

---

## Features

- Layered deterministic physiology engine
- Real-time voice-reactive excitation
- Organic entropy injection
- Updated real-time GUI dashboard
- Hot-swappable configuration
- Local LLM support (bridge ready for reconnection)
- Clean minimal runtime

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
│   └── orp_gui.py          # Updated
│
└── modules/
    ├── __init__.py
    ├── config_loader.py
    ├── osc_vrc_bridge.py
    ├── physiology.py
    ├── state.py
    ├── vrchat_output.py
    └── llm_bridge_lmstudio.py   # Legacy - disconnected
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

## Design Principles

- Deterministic over interpolated
- Readable & debuggable
- Minimal core, high expandability
- No hidden middleware or spaghetti

---

## License

**GNU Affero General Public License v3.0 (AGPL-3.0)**

**Want me to make any changes** (add screenshots section, make it shorter, more technical, etc.) before you push? Or just "**push it**"?

# ORP VRC-OSC

ORP VRC-OSC is a modular OSC middleware framework for VRChat avatars.

The project was designed around deterministic state synthesis instead of traditional parameter blending.  
Rather than forcing all telemetry sources into one shared numerical space, the framework separates avatar physiology into isolated signal layers and merges them through a controlled synthesis bus.

This allows stable expansion without rewriting core logic.

---

# Core Philosophy

ORP VRC-OSC treats avatar state as layered middleware:

| Layer | Purpose |
|---|---|
| Observation Layer | Passive environmental scanning |
| Locomotion Layer | Active movement state |
| Voice Layer | High-priority transient excitation |
| Entropy Layer | Organic jitter / realism |
| Safety Layer | Hard override / shutdown |

The framework enforces deterministic transition boundaries:

- `0.00 → 0.50` = Observation domain
- `0.51 → 1.00` = Locomotion domain

This prevents overlap between passive and active states.

---

# Features

- Modular OSC middleware architecture
- Deterministic locomotion gating
- Observation vs locomotion separation
- Voice excitation bypass system
- Organic entropy synthesis
- Safe Mode override
- VRChat OSC integration
- VRCFury sync support
- Expandable sensor pipeline
- Modular runtime loading
- Hot-swappable configuration files

---

# State Definitions

Default hue mapping:

| State | Hue |
|---|---|
| ACTIVE | `0.0` |
| CALM_MOVING | `0.3` |
| SAFE_MODE | `0.475` |
| CALM | `0.65` |

---

# Modular Architecture

```text
ORP-VRC-OSC/
│
├── osc_bridge.py
├── physiology.py
│
├── modules/
│   ├── voice.py
│   ├── locomotion.py
│   ├── observation.py
│   ├── heartbeat.py
│   ├── vision.py
│   └── safety.py
│
├── config/
│   ├── hues.json
│   ├── thresholds.json
│   └── runtime.json
│
├── launch/
│   ├── launch.bat
│   └── launch_debug.bat
│
├── LICENSE
└── README.md
````

---

# Signal Bus Design

## Observation Layer

Passive telemetry:

* Head rotation
* Camera movement
* Environmental scanning

Restricted to:

```text
0.00 → 0.50
```

This layer never activates locomotion.

---

## Locomotion Layer

Physical motion telemetry:

* VelocityMagnitude
* Movement inertia
* Ground energy

Restricted to:

```text
0.51 → 1.00
```

This acts as the hard activation threshold.

---

## Voice Layer

Voice is treated as a high-priority interrupt bus.

It bypasses locomotion gating entirely.

Voice affects:

* CoreGlow
* SensoryGlow

without requiring movement activation.

---

# OSC Ports

Default routing:

| Direction    | Port   |
| ------------ | ------ |
| VRChat → ORP | `9005` |
| ORP → VRChat | `9000` |

---

# Requirements

Python 3.10+

Install dependencies:

```bash
pip install python-osc
```

---

# Launch

Windows:

```bat
launch\launch.bat
```

---

# Example Runtime

```text
🚀 ORP VRC-OSC Online
Observation Layer Active
Locomotion Gate Stable
Voice Excitation Bus Online
Heartbeat Middleware Ready
```

---

# License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

Commercial closed-source forks are prohibited.

Any distributed or networked modification must remain open-source under the same license.

See `LICENSE` for full terms.

---

# Design Notes

This framework intentionally avoids:

* parameter spaghetti
* uncontrolled interpolation
* unstable state blending
* hidden middleware
* hardcoded monolithic logic

The goal is deterministic avatar physiology middleware.

---

# Warning

This framework directly manipulates VRChat OSC avatar parameters.

Use responsibly.

You are responsible for:

* avatar safety
* parameter validation
* OSC routing stability
* runtime testing

---

# Credits

Created by Laurentius Maximus.

ORP Framework Architecture:

* Deterministic middleware synthesis
* Layered physiology bus
* Threshold-gated state topology
* Modular telemetry routing



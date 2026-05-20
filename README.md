# ORP VRC-OSC

ORP VRC-OSC is a modular OSC middleware runtime for VRChat avatars built around deterministic physiology synthesis, layered telemetry, and scalable sensor-bus architecture.

This project transforms avatar control from simple animation toggles into a structured real-time middleware platform.

---

# Philosophy

ORP VRC-OSC is built around several engineering principles:

- deterministic runtime behavior
- modular middleware architecture
- strict signal isolation
- layered state telemetry
- hardware-safe synthesis
- scalable physiology systems

The runtime treats avatar systems like a distributed telemetry stack instead of disconnected animation drivers.

---

# Features

## Deterministic Glow Architecture

Glow synthesis is separated into two mathematically isolated domains:

| Layer | Range | Purpose |
|---|---|---|
| Observation Layer | `0.00 → 0.50` | Passive scanning / head movement |
| Locomotion Layer | `0.51 → 1.00` | Active movement / kinetic state |

This creates a hard threshold between passive and active states.

---

## Modular Sensor Buses

Each subsystem operates independently before feeding into the synthesis runtime.

Current buses:

- Voice excitation
- Locomotion
- Observation / head movement
- Entropy / jitter
- Sync heartbeat

Planned buses:

- Heartbeat
- Eye tracking
- Vision
- Stress telemetry
- Environmental response
- Presence detection

---

## State Telemetry via MainHue

`MainHue` functions as a high-level telemetry channel.

| State | Hue |
|---|---|
| ACTIVE | `0.0` |
| CALM_MOVING | `0.3` |
| SAFE_MODE | `0.475` |
| CALM | `0.65` |

Hard clamps prevent floating-point drift and parameter flicker.

---

# Architecture

```text
VRCRouter/
│
├── osc_bridge.py
├── launch.bat
│
├── config/
│   └── hues.py
│
├── core/
│   ├── state.py
│   ├── parameters.py
│   ├── transport.py
│   └── utils.py
│
├── modules/
│   ├── physiology.py
│   ├── locomotion.py
│   ├── observation.py
│   ├── voice.py
│   ├── sync.py
│   ├── modes.py
│   └── handlers.py
│
└── runtime/
    └── update_loop.py
```

---

# Runtime Model

ORP behaves like a layered middleware stack.

| Layer | Function |
|---|---|
| Physical Layer | Locomotion gate |
| Observation Layer | Head telemetry |
| Transport Layer | Voice excitation |
| Application Layer | Entropy / jitter |
| Synthesis Layer | Physiology output |

This prevents sensor collision and procedural parameter spaghetti.

---

# Installation

## Requirements

- Python 3.10+
- VRChat OSC enabled
- python-osc

Install dependency:

```bash
pip install python-osc
```

---

# Startup

Run:

```bat
launch.bat
```

Or directly:

```bash
python osc_bridge.py
```

---

# OSC Ports

| Purpose | Port |
|---|---|
| VRChat Output | `9000` |
| Runtime Input | `9005` |

---

# Current Parameter Outputs

| Parameter | Type |
|---|---|
| MainHue | float |
| CoreGlow | float |
| SensoryGlow | float |
| GroundGlow | float |
| BreathingOn | bool |
| TailWag | bool |

---

# Sensor Inputs

| Input | Purpose |
|---|---|
| Voice | Excitation bus |
| VelocityMagnitude | Locomotion |
| AngularY | Observation layer |
| Earmuffs | Calm mode |
| SafeMode | Runtime suppression |
| VF52 Sync | Heartbeat validation |

---

# Design Goals

The project is designed around:

- deterministic synthesis
- modular architecture
- scalable middleware
- stable threshold gating
- future hardware integration
- physiology abstraction

The runtime intentionally avoids:

- parameter blending chaos
- uncontrolled interpolation
- hidden state coupling
- monolithic runtime structures

---

# Planned Modules

Future integrations:

- Heartbeat synthesis
- Eye tracking
- Stress telemetry
- Environmental adaptation
- Biometric integration
- Distributed OSC networking
- Multi-avatar synchronization

---

# Project Status

Current status:

- Stable modular architecture
- Deterministic locomotion gate
- Observation/locomotion separation complete
- Middleware foundation operational

---

# License

This project is licensed under the:

GNU Affero General Public License v3.0 (AGPLv3)

All derivative works must:
- preserve attribution
- remain open-source
- disclose modifications
- maintain AGPL licensing

This ensures ORP remains open middleware infrastructure and cannot be silently absorbed into proprietary systems.

---

# Author

Laurentius Maximus

ORP Runtime Architecture / Physiology Middleware System

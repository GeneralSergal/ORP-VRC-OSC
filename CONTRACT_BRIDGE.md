# ORP Cross-Repository Contract Bridge v0.1

## Purpose
This file defines the formal relationship between ORP repositories and runtime implementations to prevent architectural drift.

## Layer Definitions

- **L4 — Planning Layer**: Vision documents, CRA blocks, future concepts  
  → Advisory only.

- **L3 — Specification Layer**: Main ORP repository (`GeneralSergal/ORP`)  
  → Source of truth for governance, protocols, and invariants.

- **L2 — Reference Implementation**: `ORP-Reference-kit`  
  → Executable validation, CTS, golden traces.

- **L1 — Runtime**: This project (`ORP-VRC-OSC`) and other deployed instances.

## Propagation Rules

1. L4 proposals must be reviewed before entering L3.
2. L3 changes must be reflected in L2 (Reference-kit) before L1 runtimes.
3. All major changes in this runtime (L1) should reference this bridge.
4. "Implementation Delta" must be documented when deviating from Reference-kit.

## Current Status (2026-05-23)

- **SHS**: YELLOW (Creative Mischief Mode)
- **DRIFT**: LOW
- **LAS**: L2/L3 Active
- **Protocol**: 0.51_STRICT

Approved by: Architect & Herald of Darkness  
Last Updated: 2026-05-23
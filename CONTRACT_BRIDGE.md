# ORP Cross-Repository Contract Bridge

## Version ORP Bridge Contract v1.0

---

## 1. PURPOSE

This document defines the strict boundary between:

- ORP Spec Repository ([`ORP`](https://github.com/GeneralSergal/ORP))
- ORP Execution Repository ([`ORP-Reference-kit`](https://github.com/GeneralSergal/ORP-Reference-kit))
- ORP VRChat OSC Runtime ([`ORP-VRC-OSC`](https://github.com/GeneralSergal/ORP-VRC-OSC))

It prevents implicit coupling between:
- governance specification
- runtime implementation
- CTS validation expectations
- live deployment behavior

---

## 2. LAYER OWNERSHIP MODEL

### L3 — SPECIFICATION ([`ORP`](https://github.com/GeneralSergal/ORP))
- Defines system invariants
- Defines governance semantics
- Defines conceptual architecture
- MUST NOT define runtime behavior details
- MUST NOT define CTS expectations

---

### L2 — EXECUTION ([`ORP-Reference-kit`](https://github.com/GeneralSergal/ORP-Reference-kit))
- Implements deterministic runtime behavior
- Owns execution logic
- Owns CTS harness implementation
- MUST NOT redefine specification invariants

---

### L1 — RUNTIME ([`ORP-VRC-OSC`](https://github.com/GeneralSergal/ORP-VRC-OSC))
- Live deployment of ORP governance in VRChat via OSC
- Consumes L2 reference implementation as its execution contract
- Produces observed execution traces and session telemetry
- MUST NOT redefine spec invariants or CTS expectations

#### L1 Runtime Output
- Observed execution traces
- Golden runs
- Regression artifacts
- Immutable once generated per version

---

## 3. CTS AUTHORITY RULE

The CTS (Compliance Test Suite):

- is defined in [`ORP-Reference-kit`](https://github.com/GeneralSergal/ORP-Reference-kit) ONLY
- is NOT a spec authority
- is a validation tool, not a truth source

CTS failures indicate:
- implementation drift OR
- spec/implementation mismatch

NOT spec invalidity.

---

## 4. CHANGE PROPAGATION RULE

Any change MUST follow:

1. Spec change ([`ORP`](https://github.com/GeneralSergal/ORP))
   ↓
2. Manual review / translation step
   ↓
3. Implementation update ([`ORP-Reference-kit`](https://github.com/GeneralSergal/ORP-Reference-kit))
   ↓
4. CTS update ONLY if behavior contract changes
   ↓
5. Golden run regeneration ONLY if explicitly approved

---

## 5. FORBIDDEN PATHS

The following are explicitly disallowed:

- CTS defining spec behavior
- Runtime behavior defining spec truth
- Golden traces silently redefining invariants
- L4 planning artifacts directly altering CTS expectations

---

## 6. DRIFT RESOLUTION RULE

If CTS fails:

Classify root cause as one of:

- IMPLEMENTATION_DRIFT
- SPEC_MISMATCH
- TEST_STALE

Resolution must explicitly declare which category applies.

---

## 7. VERSIONING RULE

- [`ORP`](https://github.com/GeneralSergal/ORP) spec versioning is independent of reference-kit versioning
- [`ORP-Reference-kit`](https://github.com/GeneralSergal/ORP-Reference-kit) may lag spec by one major version
- CTS version must match [`ORP-Reference-kit`](https://github.com/GeneralSergal/ORP-Reference-kit) version exactly

---

## 8. FINAL AUTHORITY STATEMENT

No repository has global authority.

Authority is partitioned:

- Spec defines intent
- Implementation defines behavior
- CTS verifies consistency between them
- Runtime defines observed truth

---

## License

GNU General Public License v3.0 (GPL-3.0)

Copyright 2026 Laurentius Maximus ENTROPIA

This file is part of ORP — Open Resonance Protocol, licensed under the GNU General Public License v3.0.
See the [LICENSE](LICENSE) file for full terms.

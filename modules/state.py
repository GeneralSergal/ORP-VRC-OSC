import threading

state_lock = threading.Lock()

# Centralized State Bus
state = {
    # STT Control
    "stt_enabled": True,

    # Inputs (from osc_vrc_bridge)
    "Earmuffs": 1,
    "VelocityMagnitude": 0.0,
    "Voice": 0.0,
    
    # Internal Synthesis State
    "state": "CALM",
    
    # Outputs (to vrchat_output)
    "MainHue": 0.65,
    "CoreGlow": 0.0,
    "SensoryGlow": 0.0,
    "GroundGlow": 0.0,
    "BreathingOn": 0,
    "TailWag": 0
}
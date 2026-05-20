import threading

state_lock = threading.Lock()

state = {
    # Input readings
    "Earmuffs": 0,
    "VelocityMagnitude": 0.0,
    "voice_input": 0.0,
    "head_input": 0.0,

    # Internal energy states
    "ground_energy": 0.0,
    "core_energy": 0.0,
    "sensory_energy": 0.0,

    # Outputs
    "MainHue": 0.0,
    "CoreGlow": 0.0,
    "SensoryGlow": 0.0,
    "GroundGlow": 0.0,
    "BreathingOn": 0,
    "TailWag": 0,

    # Movement state
    "state": "CALM"
}
import threading
import time
import random
from .state import state, state_lock

TICK_RATE = 0.05
HUES = {"ACTIVE": 0.0, "CALM_MOVING": 0.30, "SAFE_MODE": 0.475, "CALM": 0.65}

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def smooth(current, target, speed=0.08): return current + ((target - current) * speed)

def physiology_loop():
    print("[ ORP ] Physiology system online")
    while True:
        with state_lock:
            earmuffs = int(state.get("Earmuffs", 1))
            velocity = float(state.get("VelocityMagnitude", 0.0))
            voice = float(state.get("Voice", 0.0))
            
            movement = clamp(velocity / 4.0)
            
            # State Logic
            if earmuffs == 0: current = "ACTIVE"
            elif movement > 0.08: current = "CALM_MOVING"
            else: current = "CALM"
            
            state["state"] = current
            
            # Hue Precision Snap-to-Grid
            target_hue = HUES.get(current, 0.65)
            current_hue = float(state.get("MainHue", 0.65))
            if abs(current_hue - target_hue) < 0.005:
                state["MainHue"] = target_hue
            else:
                state["MainHue"] = clamp(smooth(current_hue, target_hue, 0.08))

            # Glow Synthesis
            state["GroundGlow"] = clamp(smooth(float(state.get("GroundGlow", 0.0)), movement, 0.10))
            state["SensoryGlow"] = clamp(smooth(float(state.get("SensoryGlow", 0.0)), voice, 0.10))
            
            core_target = (state["GroundGlow"] * 0.55) + (state["SensoryGlow"] * 0.45)
            flicker = random.uniform(-0.015, 0.015)
            state["CoreGlow"] = clamp(smooth(float(state.get("CoreGlow", 0.0)), core_target + flicker, 0.08))
            
            # Booleans
            state["BreathingOn"] = int(state["CoreGlow"] > 0.02)
            state["TailWag"] = int(movement > 0.20)
            
        time.sleep(TICK_RATE)

def start_physiology():
    threading.Thread(target=physiology_loop, daemon=True).start()
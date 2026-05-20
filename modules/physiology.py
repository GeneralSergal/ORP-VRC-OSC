import threading
import time
import random

from .state import state, state_lock

# =========================================================
# CONFIG
# =========================================================

TICK_RATE = 0.05

HUES = {
    "ACTIVE": 0.0,
    "CALM_MOVING": 0.30,
    "SAFE_MODE": 0.475,
    "CALM": 0.65
}

# =========================================================
# HELPERS
# =========================================================

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def smooth(current, target, speed=0.08):
    return current + ((target - current) * speed)


# =========================================================
# LOOP
# =========================================================

def physiology_loop():

    print("[ ORP ] Physiology system online")

    while True:

        with state_lock:

            # -------------------------------------------------
            # INPUTS
            # -------------------------------------------------

            earmuffs = int(
                state.get("Earmuffs", 1)
            )

            velocity = float(
                state.get("VelocityMagnitude", 0.0)
            )

            voice = float(
                state.get("Voice", 0.0)
            )

            # -------------------------------------------------
            # NORMALIZED MOVEMENT
            # -------------------------------------------------

            movement = clamp(
                velocity / 4.0
            )

            # -------------------------------------------------
            # STATE
            # -------------------------------------------------

            if earmuffs == 0:

                current = "ACTIVE"

            elif movement > 0.08:

                current = "CALM_MOVING"

            else:

                current = "CALM"

            state["state"] = current

            # -------------------------------------------------
            # MAIN HUE
            # -------------------------------------------------

            target_hue = HUES.get(
                current,
                0.65
            )

            current_hue = float(
                state.get("MainHue", 0.65)
            )

            main_hue = smooth(
                current_hue,
                target_hue,
                0.08
            )

            main_hue = clamp(main_hue)

            state["MainHue"] = main_hue

            # -------------------------------------------------
            # GROUND GLOW
            # -------------------------------------------------

            ground_glow = smooth(
                float(state.get("GroundGlow", 0.0)),
                movement,
                0.10
            )

            ground_glow = clamp(ground_glow)

            state["GroundGlow"] = ground_glow

            # -------------------------------------------------
            # SENSORY GLOW
            # -------------------------------------------------

            sensory_glow = smooth(
                float(state.get("SensoryGlow", 0.0)),
                voice,
                0.10
            )

            sensory_glow = clamp(sensory_glow)

            state["SensoryGlow"] = sensory_glow

            # -------------------------------------------------
            # CORE GLOW
            # -------------------------------------------------

            core_target = (
                (ground_glow * 0.55) +
                (sensory_glow * 0.45)
            )

            flicker = random.uniform(
                -0.015,
                0.015
            )

            core_glow = smooth(
                float(state.get("CoreGlow", 0.0)),
                core_target + flicker,
                0.08
            )

            core_glow = clamp(core_glow)

            state["CoreGlow"] = core_glow

            # -------------------------------------------------
            # BOOLEANS
            # -------------------------------------------------

            state["BreathingOn"] = int(
                core_glow > 0.02
            )

            state["TailWag"] = int(
                movement > 0.20
            )

        time.sleep(TICK_RATE)


# =========================================================
# START
# =========================================================

def start_physiology():

    threading.Thread(
        target=physiology_loop,
        daemon=True
    ).start()
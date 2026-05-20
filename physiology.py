import time
import random

from state import state
from state import AvatarState

# =========================================================
# PARAMETERS
# =========================================================
parameters = {
    "MainHue":      {"type": "float", "value": 0.0},
    "CoreGlow":     {"type": "float", "value": 0.0},
    "SensoryGlow":  {"type": "float", "value": 0.0},
    "GroundGlow":   {"type": "float", "value": 0.0},

    "BreathingOn":  {"type": "bool", "value": True},
    "TailWag":      {"type": "bool", "value": False},
}

# =========================================================
# USER-DEFINED HUE MAP
# =========================================================
HUE_ACTIVE = 0.0
HUE_MOVING_CALM = 0.3
HUE_SAFE = 0.475
HUE_CALM = 0.65

# =========================================================
# STATE CONFIG
# =========================================================
state_config = {
    AvatarState.CALM: {
        "targets": {
            "MainHue": HUE_CALM,

            "CoreGlow": 0.0,
            "SensoryGlow": 0.0,
            "GroundGlow": 0.0,

            "BreathingOn": False,
            "TailWag": False
        },
        "jitter": 0.007
    },

    AvatarState.ACTIVE: {
        "targets": {
            "MainHue": HUE_ACTIVE,

            "CoreGlow": 0.0,
            "SensoryGlow": 0.0,
            "GroundGlow": 0.0,

            "BreathingOn": True,
            "TailWag": True
        },
        "jitter": 0.019
    },

    AvatarState.SAFE_MODE: {
        "targets": {
            "MainHue": HUE_SAFE,

            "CoreGlow": 0.0,
            "SensoryGlow": 0.0,
            "GroundGlow": 0.0,

            "BreathingOn": False,
            "TailWag": False
        },
        "jitter": 0.0
    }
}

# =========================================================
# GLOW DOMAIN MAPPING
#
# Passive  = 0.0 -> 0.50
# Active   = 0.51 -> 1.00
# =========================================================
def glow_domain(param_name, value, active_mode):
    value = max(0.0, min(1.0, value))

    domains = {
        "CoreGlow": {
            "passive": (0.10, 0.40),
            "active":  (0.51, 1.00)
        },

        "SensoryGlow": {
            "passive": (0.15, 0.50),
            "active":  (0.51, 1.00)
        },

        "GroundGlow": {
            "passive": (0.05, 0.35),
            "active":  (0.51, 0.90)
        }
    }

    if param_name not in domains:
        return value

    bounds = (
        domains[param_name]["active"]
        if active_mode
        else domains[param_name]["passive"]
    )

    return bounds[0] + (value * (bounds[1] - bounds[0]))

# =========================================================
# MAIN UPDATE LOOP
# =========================================================
def update_loop():

    while True:

        now = time.time()

        is_safe = state["safe_mode"]

        current_enum = (
            AvatarState.SAFE_MODE
            if is_safe
            else state["current"]
        )

        config = state_config[current_enum]
        targets = config["targets"]

        active_mode = (
            state["current"] == AvatarState.ACTIVE
            and not is_safe
        )

        is_alive = (
            now - state["last_sync_time"]
        ) < 5.0

        # =================================================
        # DECAY SYSTEMS
        # =================================================
        state["excitation"] *= 0.985
        state["movement_energy"] *= 0.92
        state["head_energy"] *= 0.88

        state["movement_smoothed"] += (
            state["movement_energy"]
            - state["movement_smoothed"]
        ) * 0.085

        # =================================================
        # FLICKER
        # =================================================
        flicker_modifier = 1.0

        if is_alive and (
            now - state["flicker_trigger"]
        ) < 0.15:

            flicker_modifier = random.uniform(
                0.82,
                1.08
            )

        # =================================================
        # PARAMETER PIPELINE
        # =================================================
        for name, data in parameters.items():

            target = targets.get(
                name,
                False if data["type"] == "bool" else 0.0
            )

            # =================================================
            # FLOAT PARAMETERS
            # =================================================
            if data["type"] == "float":

                # -------------------------------------------------
                # MAIN HUE
                #
                # Separate from glow system
                # -------------------------------------------------
                if name == "MainHue":

                    # Calm + Moving
                    if (
                        current_enum == AvatarState.CALM
                        and state["movement_smoothed"] > 0.035
                    ):
                        target = HUE_MOVING_CALM

                    data["value"] += (
                        target - data["value"]
                    ) * 0.048

                    send_value = data["value"]

                    # HARD CLAMP
                    if abs(send_value) < 0.00001:
                        send_value = 0.0

                # -------------------------------------------------
                # GLOW SYSTEM
                # -------------------------------------------------
                else:

                    speed = (
                        0.085
                        if name == "SensoryGlow"
                        else 0.048
                    )

                    data["value"] += (
                        target - data["value"]
                    ) * speed

                    # =============================================
                    # OBSERVATION LAYER
                    # =============================================
                    observation_layer = (
                        min(
                            0.50,
                            state["head_energy"] * 0.50
                        )
                        if active_mode
                        else 0.0
                    )

                    # =============================================
                    # LOCOMOTION LAYER
                    # =============================================
                    locomotion_active = (
                        state["movement_smoothed"] > 0.035
                    )

                    locomotion_layer = (
                        0.51
                        + (
                            min(
                                1.0,
                                state["movement_smoothed"]
                            ) * 0.49
                        )
                        if locomotion_active
                        else 0.0
                    )

                    # =============================================
                    # STATE SYNTHESIS
                    # =============================================
                    aggregated_value = (
                        locomotion_layer
                        if locomotion_active
                        else observation_layer
                    )

                    # =============================================
                    # ORGANIC JITTER
                    # =============================================
                    jitter_range = (
                        config["jitter"]
                        * (
                            0.6
                            + 0.4 * state["entropy"]
                        )
                    )

                    aggregated_value += random.uniform(
                        -jitter_range,
                        jitter_range
                    )

                    aggregated_value = max(
                        0.0,
                        min(1.0, aggregated_value)
                    )

                    # =============================================
                    # DOMAIN REMAP
                    # =============================================
                    send_value = glow_domain(
                        name,
                        aggregated_value,
                        active_mode
                    )

                    # =============================================
                    # FLICKER
                    # =============================================
                    send_value = (
                        send_value * flicker_modifier
                        if is_alive
                        else 0.0
                    )

                    # =============================================
                    # VOICE BYPASS
                    # =============================================
                    if (
                        name in ["SensoryGlow", "CoreGlow"]
                        and state["excitation"] > 0.02
                    ):
                        send_value += state["excitation"]

                    # =============================================
                    # HARDWARE CLAMP
                    # =============================================
                    send_value = max(
                        0.0,
                        min(1.0, send_value)
                    )

                    if abs(send_value) < 0.00001:
                        send_value = 0.0

            # =================================================
            # BOOL PARAMETERS
            # =================================================
            else:

                data["value"] = target

                send_value = (
                    data["value"]
                    if is_alive
                    else False
                )

            # =================================================
            # SEND TO VRCHAT
            # =================================================
            state["vrchat_client"].send_message(
                f"/avatar/parameters/{name}",
                send_value
            )

        # =====================================================
        # ENTROPY DECAY
        # =====================================================
        state["entropy"] *= 0.983

        if state["current"] == AvatarState.ACTIVE:
            state["entropy"] = max(
                state["entropy"],
                0.18
            )

        time.sleep(0.016)
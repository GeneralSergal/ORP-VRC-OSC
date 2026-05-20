import threading
import time
from pythonosc.udp_client import SimpleUDPClient

from .state import state, state_lock

# =========================================================
# CONFIG
# =========================================================

OSC_IP = "127.0.0.1"

# IMPORTANT:
# OUTPUT TO VRCHAT
OSC_PORT = 9000

TICK_RATE = 0.033

# =========================================================
# HELPERS
# =========================================================

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


# =========================================================
# OUTPUT LOOP
# =========================================================

def vrchat_output_loop():

    client = SimpleUDPClient(
        OSC_IP,
        OSC_PORT
    )

    print(f"[ ORP ] VRChat Output Active ({OSC_PORT})")

    while True:

        try:

            with state_lock:

                main_hue = clamp(
                    state.get("MainHue", 0.65)
                )

                core_glow = clamp(
                    state.get("CoreGlow", 0.0)
                )

                sensory_glow = clamp(
                    state.get("SensoryGlow", 0.0)
                )

                ground_glow = clamp(
                    state.get("GroundGlow", 0.0)
                )

                breathing = int(
                    state.get("BreathingOn", 0)
                )

                tailwag = int(
                    state.get("TailWag", 0)
                )

            # -------------------------------------------------
            # SEND OSC
            # -------------------------------------------------

            client.send_message(
                "/avatar/parameters/MainHue",
                float(main_hue)
            )

            client.send_message(
                "/avatar/parameters/CoreGlow",
                float(core_glow)
            )

            client.send_message(
                "/avatar/parameters/SensoryGlow",
                float(sensory_glow)
            )

            client.send_message(
                "/avatar/parameters/GroundGlow",
                float(ground_glow)
            )

            client.send_message(
                "/avatar/parameters/BreathingOn",
                int(breathing)
            )

            client.send_message(
                "/avatar/parameters/TailWag",
                int(tailwag)
            )

        except Exception as e:

            print(f"[ ORP ] Output Error: {e}")

        time.sleep(TICK_RATE)


# =========================================================
# START
# =========================================================

def start_vrchat_output():

    threading.Thread(
        target=vrchat_output_loop,
        daemon=True
    ).start()
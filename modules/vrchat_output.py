# =========================================================
# ORP VRChat Output Engine v2.7
# =========================================================

import time
import threading

from pythonosc.udp_client import SimpleUDPClient

from .state import state, state_lock
from .text_sanitizer import (
    sanitize_for_vrchat,
    split_chatbox_text
)

# =========================================================
# CONFIG
# =========================================================

OSC_IP = "127.0.0.1"
OSC_PORT = 9000

TICK_RATE = 0.033  # ~30 FPS

CHATBOX_LIMIT = 140
CHATBOX_DELAY = 2.4

# =========================================================
# OSC CLIENT
# =========================================================

client = SimpleUDPClient(OSC_IP, OSC_PORT)

# =========================================================
# CHATBOX
# =========================================================

chatbox_queue = []
chatbox_lock = threading.Lock()


def send_chatbox_message(text: str):
    """
    Queue a VRChat chatbox message.
    """

    if not text:
        return

    cleaned = sanitize_for_vrchat(text)

    chunks = split_chatbox_text(
        cleaned,
        CHATBOX_LIMIT
    )

    with chatbox_lock:
        chatbox_queue.extend(chunks)


def _chatbox_loop():

    while True:

        try:

            next_msg = None

            with chatbox_lock:
                if chatbox_queue:
                    next_msg = chatbox_queue.pop(0)

            if next_msg:

                client.send_message(
                    "/chatbox/input",
                    [next_msg, True, False]
                )

                print(f"[CHATBOX] {next_msg}")

                time.sleep(CHATBOX_DELAY)

            else:
                time.sleep(0.1)

        except Exception as e:
            print(f"[ ORP ] Chatbox Error: {e}")
            time.sleep(1)


# =========================================================
# AVATAR PARAM OUTPUT
# =========================================================

PARAMETER_MAP = {
    "MainHue": "/avatar/parameters/MainHue",
    "CoreGlow": "/avatar/parameters/CoreGlow",
    "SensoryGlow": "/avatar/parameters/SensoryGlow",
    "GroundGlow": "/avatar/parameters/GroundGlow",
    "BreathingOn": "/avatar/parameters/BreathingOn",
    "TailWag": "/avatar/parameters/TailWag",
}


def vrchat_output_loop():

    print(f"[ ORP ] VRChat Output Active ({OSC_PORT})")

    while True:

        try:

            with state_lock:
                snapshot = state.copy()

            for key, address in PARAMETER_MAP.items():

                if key not in snapshot:
                    continue

                value = snapshot[key]

                try:

                    if isinstance(value, bool):
                        osc_value = bool(value)

                    elif isinstance(value, int):
                        osc_value = int(value)

                    else:
                        osc_value = float(value)

                    client.send_message(address, osc_value)

                except Exception:
                    pass

        except Exception as e:
            print(f"[ ORP ] Output Error: {e}")

        time.sleep(TICK_RATE)


# =========================================================
# STARTUP
# =========================================================

def start_vrchat_output():

    threading.Thread(
        target=vrchat_output_loop,
        daemon=True
    ).start()

    threading.Thread(
        target=_chatbox_loop,
        daemon=True
    ).start()
import time
from pythonosc.udp_client import SimpleUDPClient
from .state import state, state_lock

# Configuration
OSC_IP = "127.0.0.1"
OSC_PORT = 9000
TICK_RATE = 0.033 # ~30 FPS

def vrchat_output_loop():
    client = SimpleUDPClient(OSC_IP, OSC_PORT)
    print(f"[ ORP ] VRChat Output Active ({OSC_PORT})")

    # Define the mapping of state keys to VRChat parameter addresses
    # This keeps the logic separate from the data
    parameter_map = {
        "MainHue": "/avatar/parameters/MainHue",
        "CoreGlow": "/avatar/parameters/CoreGlow",
        "SensoryGlow": "/avatar/parameters/SensoryGlow",
        "GroundGlow": "/avatar/parameters/GroundGlow",
        "BreathingOn": "/avatar/parameters/BreathingOn",
        "TailWag": "/avatar/parameters/TailWag"
    }

    while True:
        try:
            # Snapshot the state once per tick to minimize lock time
            with state_lock:
                snapshot = state.copy()

            # Iterate through the map to send updates
            for key, address in parameter_map.items():
                if key in snapshot:
                    val = snapshot[key]
                    # Clean type casting for OSC
                    client.send_message(address, val)

        except Exception as e:
            print(f"[ ORP ] Output Error: {e}")

        time.sleep(TICK_RATE)

def start_vrchat_output():
    import threading
    threading.Thread(target=vrchat_output_loop, daemon=True).start()
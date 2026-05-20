import json
import threading

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

from physiology import update_loop
from modules.handlers import earmuff_handler
from modules.handlers import safe_mode_handler
from modules.handlers import voice_handler
from modules.handlers import velocity_handler
from modules.handlers import angular_y_handler
from modules.handlers import handle_sync

from state import state

# =========================================================
# LOAD CONFIG
# =========================================================
with open("config/hues.json", "r") as f:
    config = json.load(f)

# =========================================================
# VRCHAT OUTPUT
# =========================================================
vrchat_client = SimpleUDPClient(
    "127.0.0.1",
    9000
)

state["vrchat_client"] = vrchat_client

# =========================================================
# STARTUP BANNER
# =========================================================
print("==========================================")
print("ORP VRC OSC Middleware")
print("==========================================")
print()

print("🚀 ORP Physiology Middleware Online")
print()

print("=== TELEMETRY PROFILE ===")
print()

print(f"ACTIVE        {config['ACTIVE']}")
print(f"CALM_MOVING   {config['CALM_MOVING']}")
print(f"SAFE_MODE     {config['SAFE_MODE']}")
print(f"CALM          {config['CALM']}")

print()

print("=== PIPELINE ===")
print()

print(
    f"Locomotion Threshold : "
    f"{config['PIPELINE']['locomotion_threshold']}"
)

print(
    f"Movement Smoothing   : "
    f"{config['PIPELINE']['movement_smoothing']}"
)

print(
    f"Voice Boost          : "
    f"{config['PIPELINE']['voice_boost_multiplier']}"
)

print()

print("NOTE:")
print("Manual Earmuff ON/OFF calibration may")
print("be required during startup.")
print("VRChat parameter sync can occasionally")
print("ignore initial state propagation.")

print()

# =========================================================
# START PHYSIOLOGY THREAD
# =========================================================
threading.Thread(
    target=update_loop,
    daemon=True
).start()

# =========================================================
# OSC DISPATCHER
# =========================================================
dispatcher = Dispatcher()

# ---------------------------------------------------------
# STATE CONTROL
# ---------------------------------------------------------
dispatcher.map(
    "/avatar/parameters/EarmuffInput",
    earmuff_handler
)

dispatcher.map(
    "/avatar/parameters/Earmuffs",
    earmuff_handler
)

dispatcher.map(
    "/avatar/parameters/SafeMode",
    safe_mode_handler
)

# ---------------------------------------------------------
# VOICE
# ---------------------------------------------------------
dispatcher.map(
    "/avatar/parameters/Voice",
    voice_handler
)

# ---------------------------------------------------------
# LOCOMOTION
# ---------------------------------------------------------
dispatcher.map(
    "/avatar/parameters/VelocityMagnitude",
    velocity_handler
)

# ---------------------------------------------------------
# OBSERVATION
# ---------------------------------------------------------
dispatcher.map(
    "/avatar/parameters/AngularY",
    angular_y_handler
)

# ---------------------------------------------------------
# VRCFURY SYNC
# ---------------------------------------------------------
for idx in range(4):

    dispatcher.map(
        f"/avatar/parameters/VF52_SyncIndex{idx}",
        handle_sync
    )

# =========================================================
# START OSC SERVER
# =========================================================
server = osc_server.ThreadingOSCUDPServer(
    ("127.0.0.1", 9005),
    dispatcher
)

print("OSC Server Running")
print("Listening on 127.0.0.1:9005")
print()

server.serve_forever()
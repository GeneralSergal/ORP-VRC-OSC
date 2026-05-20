import json
import threading
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc.udp_client import SimpleUDPClient

# ORP Core
from physiology import update_loop
from state import state

# Handlers
from modules.handlers import earmuff_handler
from modules.handlers import safe_mode_handler
from modules.handlers import voice_handler
from modules.handlers import velocity_handler
from modules.handlers import angular_y_handler
from modules.handlers import handle_sync

# NEW: LLM Bridge
from modules.llm_bridge_lmstudio import LMStudioBridge

# =========================================================
# LOAD CONFIG
# =========================================================
with open("config/hues.json", "r") as f:
    config = json.load(f)

# Load LLM prompts
try:
    with open("config/llm_prompts.json", "r") as f:
        llm_prompts = json.load(f)
    CORE_SYSTEM_PROMPT = llm_prompts["core_system"]
except FileNotFoundError:
    print("⚠️  llm_prompts.json not found, using fallback")
    CORE_SYSTEM_PROMPT = "You are controlling an ORP avatar. Always respond with valid JSON only."

# =========================================================
# VRCHAT OUTPUT
# =========================================================
vrchat_client = SimpleUDPClient("127.0.0.1", 9000)
state["vrchat_client"] = vrchat_client

# =========================================================
# INITIALIZE LLM BRIDGE
# =========================================================
llm = LMStudioBridge(base_url="http://localhost:1234/v1")
llm.start()

# =========================================================
# STARTUP BANNER
# =========================================================
print("==========================================")
print("ORP VRC OSC Middleware + LLM Cognitive Core")
print("==========================================")
print()
print("🚀 ORP Physiology Middleware Online")
print("🧠 LM Studio Bridge Connected")
print()
print("=== TELEMETRY PROFILE ===")
print(f"ACTIVE          {config['ACTIVE']}")
print(f"CALM_MOVING     {config['CALM_MOVING']}")
print(f"SAFE_MODE       {config['SAFE_MODE']}")
print(f"CALM            {config['CALM']}")
print()
print("=== PIPELINE ===")
print(f"Locomotion Threshold : {config['PIPELINE']['locomotion_threshold']}")
print(f"Movement Smoothing   : {config['PIPELINE']['movement_smoothing']}")
print(f"Voice Boost          : {config['PIPELINE']['voice_boost_multiplier']}")
print()
print("NOTE: LM Studio must be running on port 1234")
print()

# =========================================================
# START PHYSIOLOGY THREAD
# =========================================================
threading.Thread(target=update_loop, daemon=True).start()

# =========================================================
# OSC DISPATCHER
# =========================================================
dispatcher = Dispatcher()

# STATE CONTROL
dispatcher.map("/avatar/parameters/EarmuffInput", earmuff_handler)
dispatcher.map("/avatar/parameters/Earmuffs", earmuff_handler)
dispatcher.map("/avatar/parameters/SafeMode", safe_mode_handler)

# VOICE
dispatcher.map("/avatar/parameters/Voice", voice_handler)

# LOCOMOTION
dispatcher.map("/avatar/parameters/VelocityMagnitude", velocity_handler)

# OBSERVATION
dispatcher.map("/avatar/parameters/AngularY", angular_y_handler)

# VRCFURY SYNC
for idx in range(4):
    dispatcher.map(f"/avatar/parameters/VF52_SyncIndex{idx}", handle_sync)

# =========================================================
# START OSC SERVER
# =========================================================
server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9005), dispatcher)
print("OSC Server Running → Listening on 127.0.0.1:9005")
print("LLM Cognitive Layer Active")
print()
server.serve_forever()

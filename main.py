# =========================================================
# ORP-VRC-OSC v2.7 - OPTIMIZED RUNTIME
# Main Runtime
# =========================================================

import customtkinter as ctk 
import threading
import sys
import json
import os

# Helper to load scaling factor
def get_scale():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f).get("scale", 1.25)
        except:
            pass
    return 1.25

ctk.set_widget_scaling(get_scale())

from modules.osc_vrc_bridge import start_osc_server
from modules.physiology import start_physiology
from modules.vrchat_output import start_vrchat_output
from modules.llm_bridge_lmstudio import LMStudioBridge
from modules.logger import ORPLogger
from gui.orp_gui import ORPGUI
from modules.speech_listener import start_listening 

def main():
    logger = ORPLogger()
    print("[ORP] Boot sequence starting...")

    root = ctk.CTk() 
    root.title("ORP Dashboard v2.7 — Herald of Darkness")
    root.geometry("1280x920")

    # =====================================================
    # LLM BRIDGE
    # =====================================================
    llm_bridge = None
    try:
        llm_bridge = LMStudioBridge()
        logger.log("LLM Bridge initialized", None)
    except Exception as e:
        logger.log(f"LLM Bridge init failed: {e}", None)

    # =====================================================
    # GUI
    # =====================================================
    try:
        # ORPGUI internally handles all status updates via its own _update_loop
        app = ORPGUI(root, llm_bridge=llm_bridge)
        
        if llm_bridge:
            llm_bridge.attach_gui(app)
            
            # Start STT Listener
            try:
                start_listening(llm_bridge)
                logger.log("🎙️ Speech Recognition Online", app)
            except Exception as e:
                logger.log(f"🎙️ Speech Recognition failed to start: {e}", app)
            
        logger.log("ORP v2.7 Boot Sequence Started", app)
        logger.log("System Dashboard Online", app)
    except Exception as e:
        print(f"[ORP] GUI Initialization Error: {e}")
        import traceback
        traceback.print_exc()
        root.destroy()
        return

    # =====================================================
    # SERVICES
    # =====================================================
    services = [
        (lambda: start_osc_server(app.handle_incoming_osc, 9005), "OSC Input Server (9005)"),
        (start_physiology, "Physiology Engine"),
        (start_vrchat_output, "VRChat Output")
    ]

    for func, name in services:
        try:
            threading.Thread(target=func, daemon=True).start()
            logger.log(f"{name} Online", app)
        except Exception as e:
            logger.log(f"{name} Failed: {e}", app)

    if llm_bridge:
        logger.log("🧠 LM Studio Bridge initialized", app)
    
    logger.log("=== ORP Runtime Fully Started ===", app)
    root.mainloop()

if __name__ == "__main__":
    main()
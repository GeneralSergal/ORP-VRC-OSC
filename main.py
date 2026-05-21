# =========================================================
# ORP-VRC-OSC v2.7
# Main Runtime
# =========================================================

import tkinter as tk
import threading
import sys
import os

from modules.osc_vrc_bridge import start_osc_server
from modules.physiology import start_physiology
from modules.vrchat_output import start_vrchat_output
from modules.llm_bridge_lmstudio import LMStudioBridge
from modules.logger import ORPLogger
from gui.orp_gui import ORPGUI

def main():
    # Initialize Persistent Logger
    logger = ORPLogger()
    
    print("[ORP] Boot sequence starting...")
    root = tk.Tk()

    # =====================================================
    # LLM BRIDGE & GUI INITIALIZATION
    # =====================================================
    llm_bridge = None
    try:
        llm_bridge = LMStudioBridge()
        print("[ORP] LLM Bridge initialized")
    except Exception as e:
        print(f"[ORP] LLM Bridge init failed: {e}")

    try:
        # Initialize GUI first so it's ready for the bridge to attach
        app = ORPGUI(root, llm_bridge=llm_bridge)
        
        if llm_bridge:
            llm_bridge.attach_gui(app)
            
        # Log to both File and GUI
        logger.log("ORP v2.7 Boot Sequence Started", app)
        logger.log("System Dashboard Online", app)
    except Exception as e:
        print(f"[ORP] GUI Critical Failure: {e}")
        root.destroy()
        return

    # =====================================================
    # START BACKGROUND SERVICES
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

    # =====================================================
    # START LLM BRIDGE
    # =====================================================
    if llm_bridge:
        try:
            llm_bridge.start()
            logger.log("🧠 LM Studio Bridge ONLINE", app)
        except Exception as e:
            logger.log(f"LLM Bridge Start Failed: {e}", app)

    logger.log("=== ORP Runtime Fully Started ===", app)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[ORP] Shutdown by user.")
        sys.exit(0)
    except Exception as e:
        print(f"[ORP] Critical Failure: {e}")
        sys.exit(1)
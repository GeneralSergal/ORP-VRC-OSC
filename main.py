# =========================================================
# ORP-VRC-OSC v2.7
# Main Runtime
# =========================================================

import tkinter as tk
import threading
import sys

from modules.osc_vrc_bridge import start_osc_server
from modules.physiology import start_physiology
from modules.vrchat_output import start_vrchat_output
from modules.llm_bridge_lmstudio import LMStudioBridge
from modules.logger import ORPLogger
from gui.orp_gui import ORPGUI


def main():
    # Initialize Logger
    logger = ORPLogger()

    print("[ORP] Boot sequence starting...")

    root = tk.Tk()

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
        app = ORPGUI(root, llm_bridge=llm_bridge)
        
        if llm_bridge:
            llm_bridge.attach_gui(app)
            
        logger.log("ORP v2.7 Boot Sequence Started", app)
        logger.log("System Dashboard Online", app)
    except Exception as e:
        logger.log(f"GUI Critical Failure: {e}", None)
        root.destroy()
        return

    # =====================================================
    # BACKGROUND SERVICES
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
    # LLM BRIDGE - Manual Control Only
    # =====================================================
    if llm_bridge:
        logger.log("🧠 LM Studio Bridge initialized (use ENABLE button in LLM tab)", app)
    else:
        logger.log("🧠 LLM Bridge not available", app)

    logger.log("=== ORP Runtime Fully Started ===", app)
    logger.log("Herald of Darkness — Awake", app)

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
# =========================================================
# ORP-VRC-OSC v2.7 - OPTIMIZED RUNTIME
# =========================================================
import customtkinter as ctk
import threading
import sys
import json
import os
import time                      # ← Added this
from datetime import datetime

# ====================== GLOBAL THEME & SCALING ======================
def load_config_scale():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f).get("scale", 1.25)
    except:
        pass
    return 1.25

ctk.set_widget_scaling(load_config_scale())
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# ====================== IMPORTS ======================
from modules.osc_vrc_bridge import start_osc_server
from modules.physiology import start_physiology
from modules.vrchat_output import start_vrchat_output
from modules.llm_bridge_lmstudio import LMStudioBridge
from modules.logger import ORPLogger
from gui.orp_gui import ORPGUI
from modules.speech_listener import start_listening

# NEW: Health Monitoring
from modules.health import health

# Import state safely
try:
    from state import state
except ImportError:
    try:
        from modules.state import state
    except ImportError:
        state = {"excitation": 0.0, "entropy": 0.0}

def main():
    logger = ORPLogger()
    print("[ORP] Boot sequence starting...")

    root = ctk.CTk()
    root.title("ORP Dashboard v2.7 — Herald of Darkness")
    root.geometry("1320x960")

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
    except Exception as e:
        print(f"[ORP] GUI Critical Failure: {e}")
        import traceback
        traceback.print_exc()
        root.destroy()
        return

    # =====================================================
    # HEALTH MONITORING (SHS + Drift)
    # =====================================================
    def health_monitor():
        while True:
            try:
                excitation = getattr(state, 'excitation', 0.0) if hasattr(state, 'excitation') else state.get("excitation", 0.0)
                entropy = getattr(state, 'entropy', 0.0) if hasattr(state, 'entropy') else state.get("entropy", 0.0)
                
                health.update(
                    excitation=excitation,
                    entropy=entropy,
                    llm_active=llm_bridge is not None
                )
                
                if hasattr(app, 'update_health_status'):
                    app.update_health_status(health.get_status())
            except Exception as e:
                print(f"[Health Monitor] Minor error: {e}")
            
            time.sleep(8)

    threading.Thread(target=health_monitor, daemon=True).start()
    logger.log("🩺 Session Health System (SHS + Drift) Online", app)

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
    # SPEECH RECOGNITION (STT)
    # =====================================================
    if llm_bridge:
        try:
            start_listening(llm_bridge)
            logger.log("🎙️ Speech Recognition Online", app)
        except Exception as e:
            logger.log(f"🎙️ Speech Recognition failed: {e}", app)

    # =====================================================
    # FINAL BOOT
    # =====================================================
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
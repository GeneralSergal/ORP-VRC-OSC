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

from gui.orp_gui import ORPGUI


def main():

    print("[ORP] Boot sequence starting...")

    root = tk.Tk()

    # =====================================================
    # LLM BRIDGE
    # =====================================================

    try:

        llm_bridge = LMStudioBridge()

        llm_bridge.gui_callback = None

        print("[ORP] LLM Bridge initialized")

    except Exception as e:

        print(f"[ORP] LLM Bridge init failed: {e}")

        llm_bridge = None

    # =====================================================
    # GUI
    # =====================================================

    try:

        app = ORPGUI(
            root,
            llm_bridge=llm_bridge
        )

        if llm_bridge:
            llm_bridge.gui_callback = (
                app.receive_llm_message
            )

        app.push_log(
            "ORP v2.7 Boot Sequence Started"
        )

        app.push_log(
            "System Dashboard Online"
        )

    except Exception as e:

        print(
            f"[ORP] GUI Critical Failure: {e}"
        )

        root.destroy()

        return

    # =====================================================
    # OSC SERVER
    # =====================================================

    try:

        threading.Thread(
            target=lambda:
            start_osc_server(
                app.handle_incoming_osc,
                9005
            ),
            daemon=True
        ).start()

        app.push_log(
            "OSC Input Server Online (9005)"
        )

    except Exception as e:

        app.push_log(
            f"OSC Input Failed: {e}"
        )

    # =====================================================
    # PHYSIOLOGY
    # =====================================================

    try:

        threading.Thread(
            target=start_physiology,
            daemon=True
        ).start()

        app.push_log(
            "Physiology Engine Online"
        )

    except Exception as e:

        app.push_log(
            f"Physiology Failed: {e}"
        )

    # =====================================================
    # VRCHAT OUTPUT
    # =====================================================

    try:

        threading.Thread(
            target=start_vrchat_output,
            daemon=True
        ).start()

        app.push_log(
            "VRChat Output Online"
        )

    except Exception as e:

        app.push_log(
            f"VRChat Output Failed: {e}"
        )

    # =====================================================
    # START LLM
    # =====================================================

    if llm_bridge:

        try:

            llm_bridge.start()

            app.llm_status.config(
                text="Status: ENABLED ✓",
                fg="green"
            )

            app.push_log(
                "🧠 LM Studio Bridge ONLINE"
            )

        except Exception as e:

            app.push_log(
                f"LLM Bridge Start Failed: {e}"
            )

    # =====================================================

    app.push_log(
        "=== ORP Runtime Fully Started ==="
    )

    app.push_log(
        "Herald of Darkness — Awake"
    )

    root.mainloop()


# =========================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n[ORP] Shutdown by user.")

        sys.exit(0)

    except Exception as e:

        print(f"[ORP] Critical Failure: {e}")

        sys.exit(1)
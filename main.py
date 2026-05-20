# =========================================================
# ORP v2.6
# MAIN RUNTIME
# =========================================================

import tkinter as tk

from modules.osc_vrc_bridge import start_osc_server
from modules.physiology import start_physiology
from modules.vrchat_output import start_vrchat_output

from gui.orp_gui import ORPGUI


# =========================================================
# MAIN
# =========================================================

def main():

    print("[ ORP ] Boot sequence starting...")

    # -----------------------------------------------------
    # OSC INPUT
    # -----------------------------------------------------

    try:

        start_osc_server()

        print("[ ORP ] OSC Input Online")

    except Exception as e:

        print(f"[ ORP ] OSC Input FAILED: {e}")

    # -----------------------------------------------------
    # PHYSIOLOGY
    # -----------------------------------------------------

    try:

        start_physiology()

        print("[ ORP ] Physiology Online")

    except Exception as e:

        print(f"[ ORP ] Physiology FAILED: {e}")

    # -----------------------------------------------------
    # VRCHAT OUTPUT
    # -----------------------------------------------------

    try:

        start_vrchat_output()

        print("[ ORP ] VRChat Output Online")

    except Exception as e:

        print(f"[ ORP ] VRChat Output FAILED: {e}")

    # -----------------------------------------------------
    # GUI
    # -----------------------------------------------------

    try:

        root = tk.Tk()

        app = ORPGUI(root)

        app.push_log("ORP Runtime Started")
        app.push_log("OSC Input Active")
        app.push_log("Physiology Active")
        app.push_log("VRChat Output Active")

        root.mainloop()

    except Exception as e:

        print(f"[ ORP ] GUI FAILED: {e}")


# =========================================================
# ENTRY
# =========================================================

if __name__ == "__main__":

    main()
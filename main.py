import tkinter as tk
import threading
import modules.osc_vrc_bridge as bridge
from modules.physiology import start_physiology
from modules.vrchat_output import start_vrchat_output
from gui.orp_gui import ORPGUI

current_osc_port = 9005

def main():
    root = tk.Tk()
    
    def log(msg):
        print(f"[ ORP ] {msg}")
        if 'app' in globals() or 'app' in locals():
            app.push_log(msg)

    def update_osc_port(new_port):
        global current_osc_port
        if new_port == current_osc_port:
            return
        
        log(f"Rebinding Network Pipeline... Switching to Port {new_port}")
        # Call shutdown on the old server instance if running
        if hasattr(bridge, 'active_server') and bridge.active_server:
            try:
                bridge.active_server.shutdown()
                bridge.active_server.server_close()
            except Exception as e:
                log(f"Clean socket disconnect trace: {e}")

        current_osc_port = new_port
        # Spin up a completely fresh network container thread on new target port
        threading.Thread(target=lambda: bridge.start_osc_server(app.handle_incoming_osc, current_osc_port), daemon=True).start()

    app = ORPGUI(root, on_port_change_callback=update_osc_port)
    log("Boot sequence starting...")

    threads = [
        ("OSC", lambda: bridge.start_osc_server(app.handle_incoming_osc, current_osc_port)), 
        ("Physiology", start_physiology), 
        ("Output", start_vrchat_output)
    ]

    for name, target in threads:
        threading.Thread(target=target, daemon=True).start()
        log(f"{name} thread initialized and running.")

    root.mainloop()

if __name__ == "__main__":
    main()
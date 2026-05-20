import threading
from pythonosc import dispatcher, osc_server
from .state import state, state_lock

OSC_IP = "127.0.0.1"
OSC_PORT = 9005  # input from VRChat

def _voice_handler(addr, value):
    with state_lock:
        state["Voice"] = float(value)

def _earmuffs_handler(addr, value):
    with state_lock:
        state["Earmuffs"] = int(value)

def _velocity_handler(addr, value):
    with state_lock:
        state["VelocityMagnitude"] = float(value)

def start_osc_server():
    disp = dispatcher.Dispatcher()
    disp.map("/avatar/parameters/Voice", _voice_handler)
    disp.map("/avatar/parameters/Earmuffs", _earmuffs_handler)
    disp.map("/avatar/parameters/VelocityMagnitude", _velocity_handler)

    server = osc_server.ThreadingOSCUDPServer(
        (OSC_IP, OSC_PORT), disp
    )

    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"[ ORP ] OSC Server Running on {OSC_IP}:{OSC_PORT}")
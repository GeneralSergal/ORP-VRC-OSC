from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient
from modules.state import state, state_lock

# Global placeholder to allow clean socket rebinding from the main loop
active_server = None

def start_osc_server(gui_callback=None, port=9005):
    """
    Initializes and starts the UDP OSC listening server.
    Intercepts data packets, updates the shared core physiology states,
    and forwards raw address streams directly to the Live Debugger GUI tab.
    """
    global active_server
    dispatcher = Dispatcher()
    
    # -------------------------------------------------------------------------
    # UNIVERSAL CATCH-ALL STREAM HANDLER
    # -------------------------------------------------------------------------
    def universal_handler(address, *args):
        value = args[0] if args else None
        
        # Cast Python booleans cleanly into numerical integers (1 or 0)
        if isinstance(value, bool):
            value = 1 if value else 0
        
        # 1. Dynamically sync parameters into your existing modules.state engine
        if address.startswith("/avatar/parameters/"):
            param_name = address.replace("/avatar/parameters/", "")
            with state_lock:
                state[param_name] = value

        # 2. Forward EVERY raw stream item directly to our UI callback handler
        if gui_callback:
            gui_callback(address, value)

    # Attach the universal catch-all handler directly to the dispatcher instance
    dispatcher.set_default_handler(universal_handler)
    
    # -------------------------------------------------------------------------
    # SOCKET RUNTIME INITIALIZATION
    # -------------------------------------------------------------------------
    listen_ip = "127.0.0.1"
    print(f"[ ORP ] OSC Server binding to {listen_ip}:{port}...")
    
    try:
        active_server = BlockingOSCUDPServer((listen_ip, port), dispatcher)
        active_server.serve_forever()
    except Exception as e:
        # Gracefully log network device blocks (e.g. WinError 10048 port conflicts)
        print(f"[ ORP ERR ] Socket failed to bind on port {port}: {e}")


def send_osc_parameter(param_name, value, vrchat_port=9000):
    """
    Creates a temporary UDP connection client and transmits a 
    custom/writable parameter alteration state message directly into VRChat.
    """
    vrc_ip = "127.0.0.1"
    address = f"/avatar/parameters/{param_name}"
    try:
        client = SimpleUDPClient(vrc_ip, vrchat_port)
        client.send_message(address, value)
        print(f"[ ORP SEND ] Transmitted {address} -> {value}")
    except Exception as e:
        print(f"[ ORP ERR ] Failed to transmit OSC packet to VRChat: {e}")
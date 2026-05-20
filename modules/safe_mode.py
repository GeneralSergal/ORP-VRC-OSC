from state import state

def safe_mode_handler(address, *args):
    if args:
        state["safe_mode"] = bool(args[0])

        print(
            f"!! SAFE MODE: {state['safe_mode']} !!"
        )
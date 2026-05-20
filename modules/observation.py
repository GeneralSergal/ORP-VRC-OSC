from state import state

def angular_y_handler(address, *args):
    if args:
        state["head_energy"] = max(
            state["head_energy"],
            min(
                1.0,
                abs(float(args[0])) / 90.0
            )
        )
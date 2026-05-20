from state import state

def velocity_handler(address, *args):
    if args:
        vel = abs(float(args[0]))

        state["movement_energy"] = max(
            state["movement_energy"],
            min(vel, 4.0) / 4.0
        )
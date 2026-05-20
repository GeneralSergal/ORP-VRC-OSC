from state import state

def voice_handler(address, *args):
    if args:
        volume = float(args[0])

        state["excitation"] = max(
            state["excitation"],
            volume * 2.5
        )
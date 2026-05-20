import time

from state import state
from state import AvatarState

last_transition = 0.0
cooldown = 0.30

def earmuff_handler(address, *args):
    global last_transition

    if not args:
        return

    incoming_toggle = bool(args[0])

    if time.time() - last_transition < cooldown:
        return

    last_transition = time.time()

    state["current"] = (
        AvatarState.CALM
        if incoming_toggle
        else AvatarState.ACTIVE
    )

    print(
        f">> STATE: {'CALM' if incoming_toggle else 'ACTIVE'}"
    )

def handle_sync(address, *args):
    if not args:
        return

    try:
        index = int(
            address.split("SyncIndex")[-1]
        )
    except (ValueError, IndexError):
        return

    value = args[0]

    try:
        val = int(value)
    except (ValueError, TypeError):
        val = 1 if bool(value) else 0

    if state["sync_indices"][index] != val:
        state["sync_indices"][index] = val

        state["last_sync_time"] = time.time()
        state["flicker_trigger"] = time.time()
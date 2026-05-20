import time

from state import state
from state import AvatarState

# =========================================================
# TRANSITION CONTROL
# =========================================================
last_transition = 0.0
cooldown = 0.30

# =========================================================
# EARMUFF HANDLER
# =========================================================
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
        f">> STATE: "
        f"{'CALM' if incoming_toggle else 'ACTIVE'}"
    )

# =========================================================
# SAFE MODE
# =========================================================
def safe_mode_handler(address, *args):

    if args:

        state["safe_mode"] = bool(args[0])

        print(
            f"!! SAFE MODE: "
            f"{state['safe_mode']} !!"
        )

# =========================================================
# VOICE
# =========================================================
def voice_handler(address, *args):

    if args:

        volume = float(args[0])

        state["excitation"] = max(
            state["excitation"],
            volume * 2.5
        )

# =========================================================
# LOCOMOTION
# =========================================================
def velocity_handler(address, *args):

    if args:

        vel = abs(float(args[0]))

        state["movement_energy"] = max(
            state["movement_energy"],
            min(vel, 4.0) / 4.0
        )

# =========================================================
# OBSERVATION
# =========================================================
def angular_y_handler(address, *args):

    if args:

        state["head_energy"] = max(
            state["head_energy"],
            min(
                1.0,
                abs(float(args[0])) / 90.0
            )
        )

# =========================================================
# VRCFURY SYNC
# =========================================================
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
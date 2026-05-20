from enum import Enum
import time

# =========================================================
# AVATAR STATES
# =========================================================
class AvatarState(Enum):
    SAFE_MODE = 0
    CALM = 1
    ACTIVE = 2

# =========================================================
# GLOBAL STATE BUS
# =========================================================
state = {
    "current": AvatarState.ACTIVE,
    "safe_mode": False,

    "entropy": 0.45,
    "excitation": 0.0,

    "movement_energy": 0.0,
    "movement_smoothed": 0.0,

    "head_energy": 0.0,

    "sync_indices": {0: 0, 1: 0, 2: 0, 3: 0},

    "last_sync_time": time.time(),
    "flicker_trigger": 0.0,

    "vrchat_client": None
}
# =========================================================
# ORP v2.6
# OSC DEBUG UTILITIES
# =========================================================

def format_osc_snapshot(snapshot):

    if not snapshot:
        return "[ NO OSC DATA ]"

    lines = []

    for key, value in sorted(
        snapshot.items()
    ):

        lines.append(
            f"{key:<45} {value}"
        )

    return "\n".join(lines)

# =========================================================
# FILTER PARAMETERS
# =========================================================

def filter_osc_parameters(
    snapshot,
    prefix=None
):

    if prefix is None:
        return dict(snapshot)

    filtered = {}

    for key, value in snapshot.items():

        if key.startswith(prefix):

            filtered[key] = value

    return filtered

# =========================================================
# SNAPSHOT STATS
# =========================================================

def osc_statistics(snapshot):

    return {

        "parameter_count": len(snapshot),

        "has_data": bool(snapshot)
    }
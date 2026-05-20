# =========================================================
# ORP v2.6
# CONFIG LOADER
# =========================================================

import json
import os

# =========================================================
# CONFIG PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATHS = {
    "hues": os.path.join(BASE_DIR, "../config/hues.json"),
    "runtime": os.path.join(BASE_DIR, "../config/runtime.json")
}

# =========================================================
# LOAD JSON SAFELY
# =========================================================

def load_json(path):
    if not os.path.isfile(path):
        print(f"[ORP] Warning: config file not found: {path}")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ORP] Error loading config {path}: {e}")
        return {}

# =========================================================
# GET CONFIG (MERGED)
# =========================================================

def get_config():
    # Load both configs
    hues = load_json(CONFIG_PATHS["hues"])
    runtime = load_json(CONFIG_PATHS["runtime"])

    # Merge safely
    config = {}

    # PIPELINE defaults
    config["PIPELINE"] = runtime.get("PIPELINE", {
        "entropy_decay": 0.95,
        "excitation_decay": 0.95,
        "movement_decay": 0.9,
        "head_decay": 0.9
    })

    # STATE_HUES defaults
    config["STATE_HUES"] = hues.get("STATE_HUES", {
        "ACTIVE": 0.0,
        "CALM_MOVING": 0.3,
        "SAFE_MODE": 0.475,
        "CALM": 0.65
    })

    # Optional GLOW_DOMAINS
    config["GLOW_DOMAINS"] = hues.get("GLOW_DOMAINS", {})

    # Merge any runtime settings (like LLM)
    config.update(runtime)

    return config
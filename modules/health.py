# modules/health.py
from datetime import datetime
import time
from modules.las import las

class SessionHealth:
    def __init__(self):
        self.state = "GREEN"
        self.drift = "NONE"
        self.last_update = time.time()
        self.focus_fragmentation = 0.0
        self.harmony_index = 0.87
        self.uptime = 0
        self.alerts = []

    def update(self, excitation=0.0, entropy=0.0, llm_active=True):
        self.uptime = int((time.time() - self.last_update) / 60)

        # Health + Drift Logic
        if entropy > 0.8:
            self.drift = "HIGH"
            self.state = "ORANGE"
            las.elevate(3)                    # Auto-escalate
        elif entropy > 0.5:
            self.drift = "MODERATE"
            self.state = "YELLOW"
        else:
            self.drift = "LOW"
            self.state = "GREEN"

        self.focus_fragmentation = min(99.9, entropy * 1.4 * 100)
        self.harmony_index = max(0.55, 0.97 - (entropy * 0.5))

        if not llm_active and len(self.alerts) < 10:
            self.alerts.append(f"LLM offline @ {datetime.now().strftime('%H:%M')}")

    def get_status(self):
        return {
            "SHS": self.state,
            "DRIFT": self.drift,
            "LAS": las.get_status(),
            "FOCUS_FRAGMENTATION": round(self.focus_fragmentation, 1),
            "HARMONY_INDEX": round(self.harmony_index, 2),
            "UPTIME_MIN": self.uptime,
            "ALERTS": self.alerts[-5:]
        }


# Global instance
health = SessionHealth()
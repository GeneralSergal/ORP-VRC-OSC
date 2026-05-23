# modules/las.py
class LayeredAuthorityStack:
    """
    ORP v2.7 - Layered Authority Stack
    Controls when higher governance layers become active.
    """
    def __init__(self):
        self.current_level = 2          # Start at L2 (normal operation)
        self.max_level = 4
        self.active_layers = {0, 1, 2}

    def elevate(self, level: int):
        """Elevate authority when drift or complexity increases"""
        if 0 <= level <= self.max_level:
            if level > self.current_level:
                self.current_level = level
                self.active_layers.add(level)
                print(f"⚡ LAS ELEVATED → L{level} Active")

    def get_status(self):
        return {
            "CURRENT_LAS": f"L{self.current_level}",
            "ACTIVE_LAYERS": sorted(list(self.active_layers)),
            "MAX_LEVEL": self.max_level
        }


# Global instance
las = LayeredAuthorityStack()
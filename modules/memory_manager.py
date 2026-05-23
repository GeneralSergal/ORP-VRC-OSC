# =========================================================
# ORP MEMORY MANAGER
# =========================================================

from collections import deque
import json

class MemoryManager:
    def __init__(self, max_exchanges=5):
        # Rolling buffer for short-term memory
        self.memory = deque(maxlen=max_exchanges)
        
    def add_interaction(self, user_text, ai_text):
        """Adds a completed interaction to the memory buffer."""
        self.memory.append({"user": user_text, "ai": ai_text})
        
    def get_context_string(self):
        """Formats memory into a string for the system prompt."""
        if not self.memory:
            return "No recent conversation history."
            
        history = ["\nRecent conversation history:"]
        for entry in self.memory:
            history.append(f"User: {entry['user']}")
            history.append(f"AI: {entry['ai']}")
        return "\n".join(history)

    def clear(self):
        self.memory.clear()
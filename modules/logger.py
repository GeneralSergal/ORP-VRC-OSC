import os
from datetime import datetime

class ORPLogger:
    def __init__(self, log_path="logs/runtime.log"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log(self, message, app=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        
        # Write to file
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
            
        # Push to GUI if app instance is provided
        if app:
            app.push_log(formatted)
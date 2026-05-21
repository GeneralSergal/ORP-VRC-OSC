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
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")
        except:
            pass
            
        # Push to GUI if available
        if app:
            try:
                app.push_log(message)   # push_log will add its own timestamp
            except:
                pass
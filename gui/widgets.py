import tkinter as tk

from .themes import *

# =========================================================
# OSC MONITOR PANEL
# =========================================================

class OSCMonitorPanel:

    def __init__(self, root):

        self.last_content = ""

        self.text = tk.Text(
            root,
            bg=BG,
            fg=TEXT,
            insertbackground=TEXT,
            font=FONT,
            relief=tk.FLAT
        )

        self.text.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # UPDATE DATA
    # =====================================================

    def update_data(self, params):

        lines = []

        for k, v in sorted(
            params.items()
        ):

            lines.append(
                f"{k:<45} {v}"
            )

        content = "\n".join(lines)

        # -------------------------------------------------
        # UPDATE ONLY IF CHANGED
        # -------------------------------------------------

        if content != self.last_content:

            self.text.delete(
                "1.0",
                tk.END
            )

            self.text.insert(
                tk.END,
                content
            )

            self.last_content = content
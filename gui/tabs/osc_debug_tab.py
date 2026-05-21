# gui/tabs/osc_debug_tab.py

import tkinter as tk
from tkinter import ttk


class OSCDebugTab:

    def __init__(self, parent):

        # =====================================================
        # ROOT FRAME
        # =====================================================

        self.frame = tk.Frame(
            parent,
            bg="#0a0a0a"
        )

        # =====================================================
        # TITLE
        # =====================================================

        title = tk.Label(
            self.frame,
            text="OSC LIVE DEBUGGER",
            fg="#00ff99",
            bg="#0a0a0a",
            font=("Consolas", 14, "bold")
        )

        title.pack(
            pady=(10, 8)
        )

        # =====================================================
        # TABLE CONTAINER
        # =====================================================

        table_frame = tk.Frame(
            self.frame,
            bg="#0a0a0a"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =====================================================
        # TREEVIEW
        # =====================================================

        self.tree = ttk.Treeview(
            table_frame,
            columns=("address", "value"),
            show="headings",
            height=28
        )

        self.tree.heading(
            "address",
            text="OSC Address"
        )

        self.tree.heading(
            "value",
            text="Value"
        )

        self.tree.column(
            "address",
            width=500,
            anchor="w"
        )

        self.tree.column(
            "value",
            width=180,
            anchor="w"
        )

        # =====================================================
        # SCROLLBAR
        # =====================================================

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # =====================================================
        # STORAGE
        # =====================================================

        self.osc_data = {}

    # =========================================================
    # OSC UPDATE
    # =========================================================

    def handle_incoming_osc(self, address, value):

        self.osc_data[address] = value

    # =========================================================
    # MAIN UPDATE
    # =========================================================

    def update(self):

        existing = {
            self.tree.item(item)["values"][0]: item
            for item in self.tree.get_children()
        }

        for address, value in self.osc_data.items():

            value_str = str(value)

            if address in existing:

                self.tree.item(
                    existing[address],
                    values=(address, value_str)
                )

            else:

                self.tree.insert(
                    "",
                    "end",
                    values=(address, value_str)
                )
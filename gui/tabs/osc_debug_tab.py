# gui/tabs/osc_debug_tab.py

import customtkinter as ctk
import os


class OSCDebugTab:

    def __init__(self, parent):

        # =====================================================
        # ROOT FRAME
        # =====================================================

        self.frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        # =====================================================
        # PATHS
        # =====================================================

        current_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.cfg_path = os.path.join(
            current_dir,
            "../../config/ignored_params.txt"
        )

        os.makedirs(
            os.path.dirname(self.cfg_path),
            exist_ok=True
        )

        # =====================================================
        # DATA
        # =====================================================

        self.ignored_addresses = self._load_ignored()

        self.osc_data = {}

        self.rows = {}

        self.checkboxes = {}

        # =====================================================
        # BUILD UI
        # =====================================================

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):

        # =====================================================
        # HEADER
        # =====================================================

        ctk.CTkLabel(
            self.frame,
            text="OSC LIVE DEBUGGER",
            font=("Segoe UI", 22, "bold")
        ).pack(
            pady=(15, 10)
        )

        # =====================================================
        # CONTROL BAR
        # =====================================================

        ctrl_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        ctrl_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        ctk.CTkButton(
            ctrl_frame,
            text="WIPE LOG",
            width=130,
            fg_color="#331B1B",
            hover_color="#5A2D2D",
            command=self.wipe_log
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            ctrl_frame,
            text="IGNORE SELECTED",
            width=170,
            fg_color="#33331B",
            hover_color="#5A5A2D",
            command=self.ignore_selected
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            ctrl_frame,
            text="VIEW IGNORE REGISTRY",
            width=190,
            fg_color="#444444",
            hover_color="#555555",
            command=self.open_ignore_registry
        ).pack(
            side="left",
            padx=5
        )

        # =====================================================
        # SCROLL FRAME
        # =====================================================

        self.scroll_frame = ctk.CTkScrollableFrame(
            self.frame,
            label_text="Live OSC Parameters"
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

    # =========================================================
    # LOAD IGNORED
    # =========================================================

    def _load_ignored(self):

        if os.path.exists(self.cfg_path):

            try:

                with open(
                    self.cfg_path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    return set(
                        line.strip()
                        for line in f
                        if line.strip()
                    )

            except Exception as e:

                print(f"[OSC] Ignore load error: {e}")

        return set()

    # =========================================================
    # SAVE IGNORED
    # =========================================================

    def _save_ignored(self):

        try:

            with open(
                self.cfg_path,
                "w",
                encoding="utf-8"
            ) as f:

                for addr in sorted(self.ignored_addresses):

                    f.write(f"{addr}\n")

        except Exception as e:

            print(f"[OSC] Ignore save error: {e}")

    # =========================================================
    # OPEN REGISTRY WINDOW
    # =========================================================

    def open_ignore_registry(self):

        try:

            if hasattr(self, "registry_win"):

                if self.registry_win.winfo_exists():

                    self.registry_win.focus()

                    return

        except:
            pass

        self.registry_win = ctk.CTkToplevel(
            self.frame
        )

        self.registry_win.title(
            "Ignored OSC Parameters"
        )

        self.registry_win.geometry(
            "520x420"
        )

        self.registry_win.grab_set()

        ctk.CTkLabel(
            self.registry_win,
            text="Ignored OSC Parameters",
            font=("Segoe UI", 18, "bold")
        ).pack(
            pady=10
        )

        list_frame = ctk.CTkScrollableFrame(
            self.registry_win,
            label_text="Registry"
        )

        list_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.registry_vars = {}

        for addr in sorted(self.ignored_addresses):

            row = ctk.CTkFrame(
                list_frame,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                pady=2
            )

            var = ctk.StringVar(
                value="off"
            )

            ctk.CTkCheckBox(
                row,
                text=addr,
                variable=var,
                onvalue=addr,
                offvalue="off"
            ).pack(
                side="left",
                padx=5
            )

            self.registry_vars[addr] = var

        ctk.CTkButton(
            self.registry_win,
            text="REMOVE SELECTED",
            fg_color="#441111",
            hover_color="#662222",
            command=lambda: self.remove_from_ignore(
                self.registry_win
            )
        ).pack(
            pady=10
        )

    # =========================================================
    # REMOVE IGNORE
    # =========================================================

    def remove_from_ignore(self, window):

        for addr, var in list(self.registry_vars.items()):

            try:

                if var.get() != "off":

                    self.ignored_addresses.discard(addr)

            except Exception as e:

                print(f"[OSC] Remove ignore error: {e}")

        self._save_ignored()

        window.destroy()

    # =========================================================
    # HANDLE OSC INPUT
    # =========================================================

    def handle_incoming_osc(self, address, value):

        try:

            if address not in self.ignored_addresses:

                self.osc_data[address] = value

        except Exception as e:

            print(f"[OSC] Incoming OSC error: {e}")

    # =========================================================
    # WIPE LOG
    # =========================================================

    def wipe_log(self):

        self.osc_data.clear()

        for widget in self.scroll_frame.winfo_children():

            widget.destroy()

        self.rows.clear()

        self.checkboxes.clear()

    # =========================================================
    # IGNORE SELECTED
    # =========================================================

    def ignore_selected(self):

        for address, checkbox in list(self.checkboxes.items()):

            try:

                if checkbox.get() == 1:

                    self.ignored_addresses.add(address)

                    if address in self.osc_data:

                        del self.osc_data[address]

                    if address in self.rows:

                        row_widget = self.rows[address].master

                        row_widget.destroy()

                        del self.rows[address]

                    del self.checkboxes[address]

            except Exception as e:

                print(f"[OSC] Ignore selected error: {e}")

        self._save_ignored()

    # =========================================================
    # UPDATE LOOP
    # =========================================================

    def update(self):

        try:

            # SAFE COPY
            for address, value in list(self.osc_data.items()):

                if address in self.ignored_addresses:
                    continue

                value_str = str(value)

                # =================================================
                # CREATE ROW
                # =================================================

                if address not in self.rows:

                    row = ctk.CTkFrame(
                        self.scroll_frame
                    )

                    row.pack(
                        fill="x",
                        pady=2,
                        padx=4
                    )

                    check = ctk.CTkCheckBox(
                        row,
                        text="",
                        width=20
                    )

                    check.pack(
                        side="left",
                        padx=8
                    )

                    self.checkboxes[address] = check

                    addr_label = ctk.CTkLabel(
                        row,
                        text=address,
                        anchor="w",
                        width=420,
                        font=("Consolas", 12)
                    )

                    addr_label.pack(
                        side="left",
                        padx=10
                    )

                    val_label = ctk.CTkLabel(
                        row,
                        text=value_str,
                        anchor="e",
                        text_color="#00FF99",
                        font=("Consolas", 12, "bold")
                    )

                    val_label.pack(
                        side="right",
                        padx=10
                    )

                    self.rows[address] = val_label

                # =================================================
                # UPDATE EXISTING
                # =================================================

                else:

                    self.rows[address].configure(
                        text=value_str
                    )

        except Exception as e:

            print(f"[OSC] Update loop error: {e}")
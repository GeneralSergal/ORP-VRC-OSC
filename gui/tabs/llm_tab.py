# gui/tabs/llm_tab.py

import tkinter as tk


class LLMTab:

    def __init__(self, parent, parent_gui, llm_bridge):

        self.parent_gui = parent_gui
        self.llm_bridge = llm_bridge

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
            text="LM STUDIO CONTROL",
            fg="#00ff99",
            bg="#0a0a0a",
            font=("Consolas", 14, "bold")
        )

        title.pack(
            pady=(10, 8)
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.status_label = tk.Label(
            self.frame,
            text="⚪ DISCONNECTED",
            fg="#ffaa00",
            bg="#0a0a0a",
            font=("Consolas", 10, "bold")
        )

        self.status_label.pack(
            pady=(0, 10)
        )

        # =====================================================
        # CONFIG PANEL
        # =====================================================

        cfg = tk.Frame(
            self.frame,
            bg="#0a0a0a"
        )

        cfg.pack(
            fill="x",
            padx=12,
            pady=6
        )

        # URL

        tk.Label(
            cfg,
            text="LM Studio URL",
            fg="#aaaaaa",
            bg="#0a0a0a",
            font=("Consolas", 9)
        ).pack(anchor="w")

        self.url_entry = tk.Entry(
            cfg,
            bg="#111111",
            fg="#00ff99",
            insertbackground="#00ff99",
            font=("Consolas", 9)
        )

        self.url_entry.pack(
            fill="x",
            pady=(0, 8)
        )

        self.url_entry.insert(
            0,
            llm_bridge.base_url
        )

        # Timeout

        tk.Label(
            cfg,
            text="Timeout",
            fg="#aaaaaa",
            bg="#0a0a0a",
            font=("Consolas", 9)
        ).pack(anchor="w")

        self.timeout_entry = tk.Entry(
            cfg,
            bg="#111111",
            fg="#00ff99",
            insertbackground="#00ff99",
            font=("Consolas", 9)
        )

        self.timeout_entry.pack(
            fill="x",
            pady=(0, 8)
        )

        self.timeout_entry.insert(
            0,
            str(llm_bridge.timeout)
        )

        # Retries

        tk.Label(
            cfg,
            text="Retries",
            fg="#aaaaaa",
            bg="#0a0a0a",
            font=("Consolas", 9)
        ).pack(anchor="w")

        self.retries_entry = tk.Entry(
            cfg,
            bg="#111111",
            fg="#00ff99",
            insertbackground="#00ff99",
            font=("Consolas", 9)
        )

        self.retries_entry.pack(
            fill="x",
            pady=(0, 8)
        )

        self.retries_entry.insert(
            0,
            str(llm_bridge.max_retries)
        )

        # =====================================================
        # PROMPT ENTRY
        # =====================================================

        self.prompt_entry = tk.Entry(
            self.frame,
            bg="#111111",
            fg="#00ff99",
            insertbackground="#00ff99",
            font=("Consolas", 10)
        )

        self.prompt_entry.pack(
            fill="x",
            padx=12,
            pady=8
        )

        self.prompt_entry.bind(
            "<Return>",
            self.send_prompt
        )

        # =====================================================
        # SEND BUTTON
        # =====================================================

        send_btn = tk.Button(
            self.frame,
            text="SEND PROMPT",
            command=self.send_prompt,
            bg="#00aa66",
            fg="#000000",
            activebackground="#00ff99",
            font=("Consolas", 10, "bold"),
            relief="flat"
        )

        send_btn.pack(
            pady=(0, 10)
        )

        # =====================================================
        # LOG BOX
        # =====================================================

        self.log_text = tk.Text(
            self.frame,
            bg="#050505",
            fg="#00ffaa",
            wrap="word",
            font=("Consolas", 9)
        )

        self.log_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # =========================================================
    # STATUS
    # =========================================================

    def update_status(self, text, color="#00ff99"):

        self.status_label.config(
            text=text,
            fg=color
        )

    # =========================================================
    # RECEIVE LOG
    # =========================================================

    def receive_llm_message(self, text):

        self.log_text.insert(
            "end",
            f"{text}\n\n"
        )

        self.log_text.see("end")

    # =========================================================
    # SEND PROMPT
    # =========================================================

    def send_prompt(self, event=None):

        text = self.prompt_entry.get().strip()

        if not text:
            return

        try:
            self.llm_bridge.base_url = (
                self.url_entry.get().strip()
            )

            self.llm_bridge.timeout = float(
                self.timeout_entry.get().strip()
            )

            self.llm_bridge.max_retries = int(
                self.retries_entry.get().strip()
            )

            self.llm_bridge.save_config()

        except Exception:
            pass

        self.llm_bridge.send_prompt(text)

        self.prompt_entry.delete(
            0,
            "end"
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):
        pass
import tkinter as tk
from tkinter import ttk

from gui.tabs.dashboard_tab import DashboardTab
from gui.tabs.osc_debug_tab import OSCDebugTab
from gui.tabs.llm_tab import LLMTab


class ORPGUI:
    def __init__(self, root, llm_bridge=None):
        self.root = root
        self.root.title("ORP Dashboard v2.7 — Herald of Darkness")
        self.root.geometry("1280x920")
        self.root.configure(bg="#0b0b0b")

        self.llm_bridge = llm_bridge
        self.accent = "#00ff99"

        # Style
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("TNotebook", background="#0b0b0b", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#111111", foreground="#bbbbbb", 
                             padding=[14, 8], font=("Consolas", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#1f1f1f")], 
                       foreground=[("selected", "#00ff99")])

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        # Tabs
        self.dashboard_tab = DashboardTab(self.notebook)
        self.osc_tab = OSCDebugTab(self.notebook)
        self.llm_tab = LLMTab(self.notebook, self, llm_bridge)

        self.notebook.add(self.dashboard_tab.frame, text=" Dashboard ")
        self.notebook.add(self.osc_tab.frame, text=" OSC Debug ")
        self.notebook.add(self.llm_tab.frame, text=" LLM ")

        # Attach bridge to GUI for callbacks
        if self.llm_bridge:
            self.llm_bridge.attach_gui(self)

        self._update_loop()

    def push_log(self, message):
        try:
            self.dashboard_tab.push_log(message)
        except:
            print(f"[GUI] {message}")

    def update_llm_status(self, text, color="#00ff99"):
        try:
            self.llm_tab.update_status(text, color)
        except Exception as e:
            print(f"[GUI] update_llm_status error: {e}")

    def handle_incoming_osc(self, address, value):
        try:
            self.osc_tab.handle_incoming_osc(address, value)
        except Exception as e:
            print(f"[GUI] OSC error: {e}")

    def receive_llm_message(self, message):
        try:
            self.llm_tab.receive_llm_message(message)
        except Exception as e:
            print(f"[LLM GUI] {e}")

    def _update_loop(self):
        try:
            self.dashboard_tab.update()
            self.osc_tab.update()
            self.llm_tab.update()
        except Exception as e:
            print(f"[GUI] Update loop error: {e}")
        self.root.after(80, self._update_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = ORPGUI(root)
    root.mainloop()
# gui/orp_gui.py
import customtkinter as ctk
from datetime import datetime

from gui.tabs.dashboard_tab import DashboardTab
from gui.tabs.osc_debug_tab import OSCDebugTab
from gui.tabs.llm_tab import LLMTab
from gui.tabs.tts_tab import TTSTab
from gui.tabs.stt_tab import STTTab
from gui.tabs.settings_tab import SettingsTab


# ====================== GLOBAL THEME SETUP ======================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")        # green fits the gremlin aesthetic nicely


class ORPGUI:
    def __init__(self, root, llm_bridge=None):
        self.root = root
        self.llm_bridge = llm_bridge

        self.root.title("ORP Dashboard v2.7 — Herald of Darkness")
        self.root.geometry("1320x960")          # Slightly larger for all tabs

        # =====================================================
        # TABVIEW
        # =====================================================
        self.tabview = ctk.CTkTabview(
            self.root,
            fg_color="transparent",
            segmented_button_fg_color="#1E1E1E",
            segmented_button_selected_color="#00ff99",
            segmented_button_selected_hover_color="#00cc77"
        )
        self.tabview.pack(fill="both", expand=True, padx=12, pady=12)

        # =====================================================
        # CREATE TABS
        # =====================================================
        self.dashboard_frame = self.tabview.add(" Dashboard ")
        self.osc_frame       = self.tabview.add(" OSC Debug ")
        self.llm_frame       = self.tabview.add(" LLM ")
        self.tts_frame       = self.tabview.add(" TTS ")
        self.stt_frame       = self.tabview.add(" STT ")
        self.settings_frame  = self.tabview.add(" Settings ")

        # =====================================================
        # INSTANTIATE TABS
        # =====================================================
        self.dashboard_tab = DashboardTab(self.dashboard_frame)
        self.osc_tab       = OSCDebugTab(self.osc_frame)
        self.llm_tab       = LLMTab(self.llm_frame, self, llm_bridge)

        tts_engine = getattr(self.llm_bridge, "tts", None) if self.llm_bridge else None
        self.tts_tab       = TTSTab(self.tts_frame, self, tts_engine)

        self.stt_tab       = STTTab(self.stt_frame, self, llm_bridge)
        self.settings_tab  = SettingsTab(self.settings_frame, self)

        # =====================================================
        # ATTACH BRIDGE
        # =====================================================
        if self.llm_bridge:
            self.llm_bridge.attach_gui(self)

        self._update_loop()

    # =========================================================
    # OSC ROUTING
    # =========================================================
    def handle_incoming_osc(self, address, value):
        try:
            if hasattr(self.osc_tab, 'handle_incoming_osc'):
                self.osc_tab.handle_incoming_osc(address, value)
        except Exception as e:
            print(f"[GUI] OSC handler error: {e}")

    # =========================================================
    # CENTRAL LOG ROUTER WITH TIMESTAMP
    # =========================================================
    def push_log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        print(formatted)

        # Dashboard (main log)
        try:
            self.dashboard_tab.push_log(formatted)
        except:
            pass

        # LLM Tab
        if any(kw in message for kw in ["USER →", "AI →", "LM Studio", "🧠", "[LLM]"]):
            try:
                self.llm_tab.receive_llm_message(formatted)
            except:
                pass

        # TTS Tab
        if any(kw in message for kw in ["[TTS]", "SPOKE", "VOICE"]):
            try:
                self.tts_tab.push_log(formatted)
            except:
                pass

        # STT Tab
        if any(kw in message for kw in ["[STT]", "[HEARING]", "Speech Recognition"]):
            try:
                self.stt_tab.push_log(formatted)
            except:
                pass

    # =========================================================
    # LLM CALLBACKS
    # =========================================================
    def receive_llm_message(self, message: str):
        self.push_log(message)

    def update_llm_status(self, text: str, color="#00ff99"):
        try:
            if hasattr(self.llm_tab, 'update_status'):
                self.llm_tab.update_status(text, color)
        except:
            pass

    # =========================================================
    # UPDATE LOOP
    # =========================================================
    def _update_loop(self):
        try: self.dashboard_tab.update()
        except: pass
        try: self.osc_tab.update()
        except: pass
        try: self.llm_tab.update()
        except: pass
        try: self.tts_tab.update()
        except: pass
        try: self.stt_tab.update()
        except: pass
        try: self.settings_tab.update()
        except: pass

        self.root.after(80, self._update_loop)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ORPGUI(root)
    root.mainloop()
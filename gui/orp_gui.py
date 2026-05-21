import customtkinter as ctk
from datetime import datetime

from gui.tabs.dashboard_tab import DashboardTab
from gui.tabs.osc_debug_tab import OSCDebugTab
from gui.tabs.llm_tab import LLMTab
from gui.tabs.tts_tab import TTSTab
from gui.tabs.stt_tab import STTTab
from gui.tabs.settings_tab import SettingsTab

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class ORPGUI:
    def __init__(self, root, llm_bridge=None):
        self.root = root
        self.llm_bridge = llm_bridge

        self.root.title("ORP Dashboard v2.7 — Herald of Darkness")
        self.root.geometry("1280x920")

        # =====================================================
        # TAB VIEW
        # =====================================================
        self.tabview = ctk.CTkTabview(
            self.root,
            fg_color="transparent",
            segmented_button_fg_color="#1E1E1E"
        )
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # =====================================================
        # TABS
        # =====================================================
        dashboard_frame = self.tabview.add("Dashboard")
        osc_frame = self.tabview.add("OSC Debug")
        llm_frame = self.tabview.add("LLM")
        tts_frame = self.tabview.add("TTS")
        stt_frame = self.tabview.add("STT")
        settings_frame = self.tabview.add("Settings")

        # =====================================================
        # TAB INSTANCES
        # =====================================================
        self.dashboard_tab = DashboardTab(dashboard_frame)
        self.osc_tab = OSCDebugTab(osc_frame)
        self.llm_tab = LLMTab(llm_frame, self, llm_bridge)

        # TTS ENGINE
        tts_engine = getattr(self.llm_bridge, "tts", None) if self.llm_bridge else None
        self.tts_tab = TTSTab(tts_frame, self, tts_engine)

        # STT ENGINE
        self.stt_tab = STTTab(stt_frame, self, llm_bridge)

        # SETTINGS
        self.settings_tab = SettingsTab(settings_frame, self)

        # =====================================================
        # ATTACH GUI
        # =====================================================
        if self.llm_bridge:
            self.llm_bridge.attach_gui(self)

        self._update_loop()

    # =========================================================
    # OSC ROUTING
    # =========================================================
    def handle_incoming_osc(self, address, value):
        try:
            if hasattr(self, 'osc_tab'):
                self.osc_tab.handle_incoming_osc(address, value)
        except Exception as e:
            print(f"[GUI] OSC handler error: {e}")

    # =========================================================
    # LOG ROUTER
    # =========================================================
    def push_log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        print(formatted)

        # Dashboard Route
        try: self.dashboard_tab.push_log(formatted)
        except: pass

        # LLM Route
        if any(m in message for m in ["USER →", "AI →", "[OSC Chatbox]", "LM Studio", "🧠"]):
            try: self.llm_tab.receive_llm_message(formatted)
            except: pass

        # TTS Route
        if any(m in message for m in ["[TTS]", "VOICE", "SPEAK"]):
            try: self.tts_tab.push_log(formatted)
            except: pass
            
        # STT Route
        if "[HEARING]" in message or "[STT]" in message:
            try: self.stt_tab.push_log(formatted)
            except: pass

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
        
        self.root.after(80, self._update_loop)

if __name__ == "__main__":
    root = ctk.CTk()
    app = ORPGUI(root)
    root.mainloop()
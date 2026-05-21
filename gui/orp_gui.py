import tkinter as tk
from tkinter import ttk
import colorsys
import os
from modules.state import state, state_lock
from modules.osc_vrc_bridge import send_osc_parameter

# DYNAMIC ABSOLUTE PATH ENGINE
GUI_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(GUI_DIR)
IGNORED_PARAMS_FILE = os.path.join(PROJECT_ROOT, "ignored_params.txt")

class ORPGUI:
    # --- STORAGE REGISTRY MANAGEMENT ---
    def load_ignored_params(self):
        if not os.path.exists(IGNORED_PARAMS_FILE): 
            try:
                with open(IGNORED_PARAMS_FILE, "w", encoding="utf-8") as f:
                    f.write("")
            except Exception: pass
            return set()
        
        try:
            with open(IGNORED_PARAMS_FILE, "r", encoding="utf-8") as f:
                return set(line.strip() for line in f if line.strip())
        except Exception: return set()

    def save_ignored_params(self):
        try:
            with open(IGNORED_PARAMS_FILE, "w", encoding="utf-8") as f:
                for param in sorted(self.ignored_params): 
                    f.write(param + "\n")
        except Exception: pass

    def __init__(self, root, on_port_change_callback=None):
        self.root = root
        self.root.title("ORP Dashboard v2.6")
        self.root.geometry("540x840")
        self.root.configure(bg="#0a0a0a")

        self.accent = "#00ff41"
        self.canvas_width = 480
        self.osc_param_data = {}  
        self.ignored_params = self.load_ignored_params()
        self.on_port_change = on_port_change_callback
        self.last_boop_val = 0

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#0a0a0a", borderwidth=0)
        style.configure("TNotebook.Tab", background="#151515", foreground="#888", font=("Consolas", 10), padding=[15, 4])
        style.map("TNotebook.Tab", background=[("selected", "#0a0a0a")], foreground=[("selected", self.accent)])

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_dash = tk.Frame(self.notebook, bg="#0a0a0a")
        self.tab_osc = tk.Frame(self.notebook, bg="#0a0a0a")
        
        self.notebook.add(self.tab_dash, text=" SYSTEM DASHBOARD ")
        self.notebook.add(self.tab_osc, text=" OSC LIVE DEBUGGER ")

        # ---------------- TAB 1: SYSTEM DASHBOARD ----------------
        self.log_text = tk.Text(self.tab_dash, height=9, width=80, state='disabled', 
                                bg="#050505", fg=self.accent, font=("Consolas", 8), 
                                relief="flat", highlightthickness=0)
        self.log_text.pack(padx=10, pady=8, fill="x")

        self.debug_frame = tk.LabelFrame(self.tab_dash, text="Live Avatar State", bg="#0a0a0a", fg="#aaa", font=("Consolas", 10))
        self.debug_frame.pack(fill="x", padx=10, pady=5)

        # Added OSCBoop to list below
        self.debug_fields = ["state", "MuteSelf", "Earmuffs", "OSCBoop", "VelocityMagnitude", "Voice", "CoreGlow", "SensoryGlow", "GroundGlow", "MainHue", "BreathingOn", "TailWag"]
        self.debug_labels = {}
        for field in self.debug_fields:
            row = tk.Frame(self.debug_frame, bg="#0a0a0a")
            row.pack(fill="x", padx=6, pady=1)
            
            if field == "Earmuffs":
                lbl = tk.Label(row, text=f"{field}: -- (Click to Toggle)", fg=self.accent, bg="#0a0a0a", font=("Consolas", 9, "underline"), cursor="hand2")
                lbl.bind("<Button-1>", lambda e: self.toggle_earmuffs_bypass())
                lbl.bind("<Enter>", lambda e: e.widget.config(fg="#ffffff"))
                lbl.bind("<Leave>", lambda e: e.widget.config(fg=self.accent))
            else:
                lbl = tk.Label(row, text=f"{field}: --", fg=self.accent, bg="#0a0a0a", font=("Consolas", 9))
                
            lbl.pack(anchor="w")
            self.debug_labels[field] = lbl

        self.visual_frame = tk.LabelFrame(self.tab_dash, text="Shader Visualization", bg="#0a0a0a", fg="#aaa", font=("Consolas", 10))
        self.visual_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.visual_frame, text="MainHue", fg="#888", bg="#0a0a0a").pack(anchor="w", padx=6)
        self.hue_canvas = tk.Canvas(self.visual_frame, width=self.canvas_width, height=18, bg="#111", highlightthickness=0)
        self.hue_canvas.pack(pady=4, padx=4)
        self.hue_bar = self.hue_canvas.create_rectangle(0, 0, self.canvas_width, 18, fill="#f00")

        self.glow_meters = {}
        for glow in ["CoreGlow", "SensoryGlow", "GroundGlow"]:
            tk.Label(self.visual_frame, text=glow, fg="#888", bg="#0a0a0a").pack(anchor="w", padx=6)
            canvas = tk.Canvas(self.visual_frame, width=self.canvas_width, height=18, bg="#111", highlightthickness=0)
            canvas.pack(pady=3, padx=4)
            bar = canvas.create_rectangle(0, 0, 0, 18, fill=self.accent)
            self.glow_meters[glow] = (canvas, bar)

        # ---------------- TAB 2: OSC LIVE DEBUGGER ----------------
        port_frame = tk.Frame(self.tab_osc, bg="#111", height=35)
        port_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        tk.Label(port_frame, text="Listener Routing Port:", fg="#aaa", bg="#111", font=("Consolas", 9)).pack(side="left", padx=5)
        
        self.port_var = tk.StringVar(value="9005")
        self.port_box = ttk.Combobox(port_frame, textvariable=self.port_var, values=["9005", "9001", "9006"], width=8, state="readonly")
        self.port_box.pack(side="left", padx=5, pady=5)
        
        tk.Button(port_frame, text="Rebind Port", command=self.trigger_port_rebind, bg="#222", fg=self.accent,
                  activebackground=self.accent, activeforeground="#000", font=("Consolas", 8, "bold"), relief="flat").pack(side="left", padx=5)

        style.configure("Treeview", background="#050505", fieldbackground="#050505", foreground="#ffffff", font=("Consolas", 9), rowheight=22)
        style.configure("Treeview.Heading", background="#151515", foreground="#aaa", font=("Consolas", 9))
        style.map("Treeview", foreground=[('selected', '#000000'), (None, '#ffffff')], background=[('selected', self.accent)])
        
        tree_frame = tk.Frame(self.tab_osc, bg="#0a0a0a")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Address", "Value"), show="headings", selectmode="extended")
        self.tree.heading("Address", text="OSC Data Parameter Routing")
        self.tree.heading("Value", text="Current Value")
        self.tree.column("Address", width=360, anchor="w")
        self.tree.column("Value", width=120, anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)

        self.tree.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self.tree, tearoff=0, bg="#151515", fg="#fff", activebackground=self.accent, activeforeground="#000")
        self.context_menu.add_command(label="Copy Row Data", command=self.copy_selected)
        self.context_menu.add_command(label="Mute / Add to Ignore List", command=self.add_to_ignore)

        ctrl_frame = tk.Frame(self.tab_osc, bg="#0a0a0a")
        ctrl_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(ctrl_frame, text="Wipe Live Log", command=self.clear_osc_data, bg="#222", fg="#ff4444", 
                  activebackground="#ff4444", activeforeground="#fff", font=("Consolas", 9), relief="flat").pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="View Ignore Registry", command=self.open_ignore_list_window, bg="#222", fg="#aaa", 
                  activebackground=self.accent, activeforeground="#000", font=("Consolas", 9), relief="flat").pack(side="right", padx=5)

        self._update_loop()

    # --- ROUTER ASYNC CALLBACK HANDLING ENGINE ---
    def push_log(self, msg):
        self.log_text.configure(state='normal')
        self.log_text.insert('end', f"{msg}\n")
        self.log_text.see('end')
        self.log_text.configure(state='disabled')

    def handle_incoming_osc(self, address, value):
        if address not in self.ignored_params:
            self.osc_param_data[address] = value

    def trigger_port_rebind(self):
        new_port = int(self.port_var.get())
        if self.on_port_change:
            self.on_port_change(new_port)

    # --- BYPASS TRANSMISSION ENGINE ---
    def toggle_earmuffs_bypass(self):
        with state_lock:
            current_native_val = state.get("Earmuffs", 0)
            new_val = 0 if current_native_val == 1 else 1
            
        send_osc_parameter("EarmuffInput", new_val)

    def clear_osc_data(self):
        self.osc_param_data.clear()
        for item in self.tree.get_children(): 
            self.tree.delete(item)

    def show_context_menu(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            if iid not in self.tree.selection(): 
                self.tree.selection_set(iid)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_selected(self):
        selected = self.tree.selection()
        if not selected: return
        text = "\n".join(f"{self.tree.item(i, 'values')[0]}\t{self.tree.item(i, 'values')[1]}" for i in selected)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def add_to_ignore(self):
        selected = self.tree.selection()
        for item_id in selected:
            addr = self.tree.item(item_id, "values")[0]
            self.ignored_params.add(addr)
            if addr in self.osc_param_data: 
                del self.osc_param_data[addr]
            self.tree.delete(item_id)
        self.save_ignored_params()

    def open_ignore_list_window(self):
        win = tk.Toplevel(self.root, bg="#0a0a0a")
        win.title("Ignore Registry")
        win.geometry("380x400")
        
        box = tk.Listbox(win, bg="#050505", fg="#fff", font=("Consolas", 9), selectbackground=self.accent, selectforeground="#000", relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=10)
        for p in sorted(self.ignored_params): 
            box.insert(tk.END, p)

        def del_selected():
            for idx in reversed(box.curselection()):
                val = box.get(idx)
                self.ignored_params.discard(val)
                box.delete(idx)
            self.save_ignored_params()

        tk.Button(win, text="Remove Selection", command=del_selected, bg="#222", fg="#ff4444", relief="flat", font=("Consolas", 9)).pack(fill="x", padx=10, pady=5)

    # --- PRIMARY SYSTEM ITERATOR LOOP ---
    def _update_loop(self):
        with state_lock:
            # 1. Update Tab 1 Fields (System Dashboard)
            for key, lbl in self.debug_labels.items():
                val = state.get(key, "--")
                
                # Added Rising Edge Detection
                if key == "OSCBoop":
                    current_int = 1 if val in [1, 1.0, True] else 0
                    if current_int == 1 and self.last_boop_val == 0:
                        self.push_log(f"[ EVENT ] Boop detected! Value: {val}")
                    self.last_boop_val = current_int
                    lbl.config(text=f"{key}: {val}", fg=self.accent)
                elif key == "MuteSelf":
                    status = "MUTED" if val == 1 else "UNMUTED" if val == 0 else "--"
                    lbl.config(text=f"{key}: {status}", fg="#ff4444" if val == 1 else self.accent)
                elif key == "Earmuffs":
                    status = "ON" if val == 1 else "OFF" if val == 0 else "--"
                    lbl.config(text=f"{key}: {status} (Click to Toggle)")
                elif isinstance(val, float):
                    lbl.config(text=f"{key}: {val:.3f}", fg=self.accent)
                else:
                    lbl.config(text=f"{key}: {val}", fg=self.accent)
            
            hue = state.get("MainHue", 0.65)
            self.hue_canvas.itemconfig(self.hue_bar, fill=self.hue_to_rgb(hue))
            
            for glow, (canvas, bar) in self.glow_meters.items():
                val = max(0.0, min(1.0, state.get(glow, 0.0)))
                canvas.coords(bar, 0, 0, int(val * self.canvas_width), 18)
                canvas.itemconfig(bar, fill=self.glow_color(val))

            # 2. Synchronize data entries directly to Spreadsheet Rows (Tab 2)
            current_tree_nodes = {self.tree.item(i, "values")[0]: i for i in self.tree.get_children()}
            for addr, val in list(self.osc_param_data.items()):
                if addr in self.ignored_params:
                    if addr in current_tree_nodes:
                        self.tree.delete(current_tree_nodes[addr])
                    continue
                
                val_str = f"{val:.4f}" if isinstance(val, float) else str(val)
                if addr in current_tree_nodes:
                    self.tree.item(current_tree_nodes[addr], values=(addr, val_str))
                else:
                    self.tree.insert("", "end", values=(addr, val_str), tags=('visible_text',))
            
            self.tree.tag_configure('visible_text', foreground='#ffffff')

        self.root.after(33, self._update_loop)

    def hue_to_rgb(self, h):
        r, g, b = colorsys.hsv_to_rgb(h % 1.0, 1.0, 1.0)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    def glow_color(self, value):
        if value <= 0.5:
            r = int((value / 0.5) * 255); g = 255
        else:
            r = 255; g = int((1 - (value - 0.5) / 0.5) * 255)
        return f"#{r:02x}{g:02x}00"
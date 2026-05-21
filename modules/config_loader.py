import tkinter as tk
from tkinter import ttk
import os

class OSCDebugTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#0a0a0a")
        
        # Define config path
        self.cfg_path = os.path.join(os.path.dirname(__file__), "cfg/ignored_params.txt")
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.cfg_path), exist_ok=True)
        
        self.ignored_addresses = self._load_ignored()
        
        self._build_ui()
        self.osc_data = {}

    def _load_ignored(self):
        """Loads ignored parameters from text file."""
        if os.path.exists(self.cfg_path):
            with open(self.cfg_path, "r", encoding="utf-8") as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    def _save_ignored(self):
        """Saves current ignored set to text file."""
        with open(self.cfg_path, "w", encoding="utf-8") as f:
            for addr in self.ignored_addresses:
                f.write(f"{addr}\n")

    def _build_ui(self):
        tk.Label(self.frame, text="OSC LIVE DEBUGGER", fg="#00ff99", bg="#0a0a0a", 
                 font=("Consolas", 14, "bold")).pack(pady=(10, 8))

        # Control Panel
        ctrl_frame = tk.Frame(self.frame, bg="#0a0a0a")
        ctrl_frame.pack(fill="x", padx=10)
        
        tk.Button(ctrl_frame, text="WIPE LIVE LOG", command=self.wipe_log, 
                  bg="#330000", fg="#ff6666", font=("Consolas", 9)).pack(side="left", padx=5)
        tk.Button(ctrl_frame, text="IGNORE SELECTED", command=self.ignore_selected, 
                  bg="#333300", fg="#ffff99", font=("Consolas", 9)).pack(side="left", padx=5)

        # Treeview
        table_frame = tk.Frame(self.frame, bg="#0a0a0a")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("address", "value"), show="headings", height=28)
        self.tree.heading("address", text="OSC Address")
        self.tree.heading("value", text="Value")
        self.tree.column("address", width=500, anchor="w")
        self.tree.column("value", width=180, anchor="w")
        
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def handle_incoming_osc(self, address, value):
        if address not in self.ignored_addresses:
            self.osc_data[address] = value

    def wipe_log(self):
        self.osc_data.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)

    def ignore_selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            address = self.tree.item(selected_item)["values"][0]
            self.ignored_addresses.add(address)
            self._save_ignored()  # Persist to file
            
            self.tree.delete(selected_item)
            if address in self.osc_data:
                del self.osc_data[address]

    def update(self):
        existing = {self.tree.item(item)["values"][0]: item for item in self.tree.get_children()}

        for address, value in self.osc_data.items():
            if address in self.ignored_addresses: continue
            
            value_str = str(value)
            if address in existing:
                self.tree.item(existing[address], values=(address, value_str))
            else:
                self.tree.insert("", "end", values=(address, value_str))
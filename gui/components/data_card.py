import customtkinter as ctk
from typing import Callable

from core.models import DataEntry, DataEntryType

class DataCard(ctk.CTkFrame):
    def __init__(
        self,
        master,
        entry: DataEntry,
        on_view_detail: Callable[[DataEntry], None],
        on_select_toggle: Callable[[DataEntry, bool], None],
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.entry = entry
        self._on_view_detail = on_view_detail
        self._on_select_toggle = on_select_toggle
        
        self.grid_columnconfigure(1, weight=1)
        
        # Checkbox for multiselect
        self.checkbox_var = ctk.BooleanVar(value=False)
        self.checkbox = ctk.CTkCheckBox(
            self,
            text="",
            variable=self.checkbox_var,
            command=self._handle_toggle,
            width=24
        )
        self.checkbox.grid(row=0, column=0, rowspan=2, padx=(10, 5), pady=10, sticky="ns")
        
        # Badges and Labels Map
        type_colors = {
            DataEntryType.SPELL: "#3498db",  # Blue
            DataEntryType.MONSTER: "#e74c3c", # Red
            DataEntryType.ITEM: "#f1c40f",   # Yellow
            DataEntryType.CLASS: "#9b59b6",  # Purple
            DataEntryType.RACE: "#1abc9c",   # Teal
            DataEntryType.BACKGROUND: "#e67e22", # Orange
            DataEntryType.FEATURE: "#34495e" # Dark Blue
        }
        bg_color = type_colors.get(self.entry.type, "#95a5a6")
        
        # Name
        self.lbl_name = ctk.CTkLabel(
            self,
            text=self.entry.name,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        self.lbl_name.grid(row=0, column=1, padx=5, pady=(10, 0), sticky="ew")
        
        # Type Badge + Source
        info_text = f"{self.entry.type.value} • {self.entry.source}"
        self.lbl_info = ctk.CTkLabel(
            self,
            text=info_text,
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color=bg_color,
            anchor="w"
        )
        self.lbl_info.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")
        
        # View Button
        self.btn_view = ctk.CTkButton(
            self,
            text="View Detail",
            width=100,
            command=self._handle_view
        )
        self.btn_view.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        
    def _handle_toggle(self):
        is_selected = self.checkbox_var.get()
        self._on_select_toggle(self.entry, is_selected)
        
    def _handle_view(self):
        self._on_view_detail(self.entry)

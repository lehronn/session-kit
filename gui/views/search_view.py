import customtkinter as ctk
import logging
import queue
import threading
from typing import List, Optional

from core.models import DataEntry, DataEntryType
from gui.components.data_card import DataCard

logger = logging.getLogger(__name__)

class SearchView(ctk.CTkFrame):
    def __init__(self, master, app_core, **kwargs):
        super().__init__(master, **kwargs)
        self.app_core = app_core
        self.search_engine = getattr(app_core, 'search_engine', None)
        
        self.selected_entries: List[DataEntry] = []
        
        self.grid_columnconfigure(0, weight=2) # Search area
        self.grid_columnconfigure(1, weight=3) # Detail area
        self.grid_rowconfigure(1, weight=1)
        
        self._search_queue = queue.Queue()
        self._is_polling = False
        self._search_thread = None
        self._batch_after_id = None
        self._result_widgets = [] 
        
        self._build_top_bar()
        self._build_results_area()
        self._build_detail_panel()
        self._start_polling()
        
    def _start_polling(self):
        if not self._is_polling:
            self._is_polling = True
            self._check_queue_poller()

    def _check_queue_poller(self):
        """Periodically check the queue for results from the background search thread."""
        try:
            while True: 
                results = self._search_queue.get_nowait()
                self.after(0, lambda r=results: self._on_search_complete(r))
        except queue.Empty:
            pass
        
        if self._is_polling:
            self.after(100, self._check_queue_poller)

    def _build_top_bar(self):
        # Spans across both columns
        self.top_bar = ctk.CTkFrame(self, height=60)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 0))
        self.top_bar.grid_columnconfigure(0, weight=1)
        
        # Search Entry
        self.entry_search = ctk.CTkEntry(
            self.top_bar,
            placeholder_text="Search for spells, monsters, items...",
            font=ctk.CTkFont(size=14)
        )
        self.entry_search.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.entry_search.bind("<Return>", lambda e: self.perform_search())
        
        # Search Button
        self.btn_search = ctk.CTkButton(
            self.top_bar,
            text="Search",
            width=80,
            command=self.perform_search
        )
        self.btn_search.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Filter OptionMenu
        type_options = ["All Types"] + [t.value for t in DataEntryType]
        self.opt_filter = ctk.CTkOptionMenu(
            self.top_bar,
            values=type_options,
            command=self._on_filter_changed
        )
        self.opt_filter.grid(row=0, column=2, padx=(0, 10), pady=10)
        self.opt_filter.set("All Types")
        
        # Export Selected
        self.btn_export = ctk.CTkButton(
            self.top_bar,
            text="Export Selected (0)",
            width=140,
            command=self.export_selected,
            state="disabled",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE")
        )
        self.btn_export.grid(row=0, column=3, padx=(0, 10), pady=10)
        
        # Loading Label (Hidden by default)
        self.lbl_loading = ctk.CTkLabel(self.top_bar, text="Searching...", text_color="#3498db")
        self.lbl_loading.grid(row=0, column=4, padx=10)
        self.lbl_loading.grid_remove()

    def _build_results_area(self):
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Configure internal canvas for more predictable scrolling
        canvas = getattr(self.scroll_frame, "_canvas", None)
        if canvas:
            canvas.configure(yscrollincrement=1) # Pixel-precision
        
    def _bind_scroll_recursive(self, widget, handler):
        """Recursively binds a scroll handler to a widget and all its components."""
        try:
            # Bind to the widget itself
            widget.bind("<MouseWheel>", handler, add="+")
            
            # Target internal CTk/Tkinter components
            for attr in ["_canvas", "_label", "_entry", "_textbox", "_checkbox", "_bg_canvas", "_text_label"]:
                obj = getattr(widget, attr, None)
                if obj and hasattr(obj, "bind"):
                    obj.bind("<MouseWheel>", handler, add="+")
            
            # Recursive pass
            for child in widget.winfo_children():
                self._bind_scroll_recursive(child, handler)
        except: pass

    def _on_mousewheel_results(self, event):
        """Directly scroll the results canvas. macOS delta is typically 1 or -1."""
        canvas = getattr(self.scroll_frame, "_canvas", None)
        if canvas:
            # On macOS, moving fingers UP (scroll down) gives negative delta in some Tkinter builds
            # but positive in others. CTk's default is -1 * delta.
            # We'll use a speed that feels natural on macOS (approx 40px per tick)
            amt = int(-40 * event.delta)
            canvas.yview_scroll(amt, "units")

    def _on_mousewheel_detail(self, event):
        """Direct scroll for the textbox."""
        # Textbox delta is line-based. -2 feels good.
        self.detail_textbox.yview_scroll(int(-2 * event.delta), "units")

    def _build_detail_panel(self):
        self.detail_frame = ctk.CTkFrame(self)
        self.detail_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.detail_frame.grid_columnconfigure(0, weight=1)
        self.detail_frame.grid_rowconfigure(0, weight=1)

        self.detail_textbox = ctk.CTkTextbox(
            self.detail_frame, 
            wrap="word", 
            font=ctk.CTkFont(size=14),
            padx=20, pady=20
        )
        self.detail_textbox.grid(row=0, column=0, sticky="nsew")
        self.detail_textbox.insert("0.0", "Select an item to view details...")
        self.detail_textbox.configure(state="disabled")
        
        # Bind scroll for details
        self.detail_textbox.bind("<MouseWheel>", self._on_mousewheel_detail)
        
    def perform_search(self):
        if not self.search_engine:
            return

        query = self.entry_search.get()
        filter_val = self.opt_filter.get()
        
        entry_types = None
        if filter_val != "All Types":
            # Find the matching DataEntryType enum
            for ext in DataEntryType:
                if ext.value == filter_val:
                    entry_types = [ext]
                    break
        
        # Show loading indicator
        self.lbl_loading.grid()
        self.btn_search.configure(state="disabled")
        
        def run_search():
            try:
                results = self.search_engine.search(query, entry_types)
                self._search_queue.put(results)
            except Exception as e:
                logger.error(f"Search thread failed: {e}")
                self._search_queue.put([])

        self._search_thread = threading.Thread(target=run_search, daemon=True)
        self._search_thread.start()

    def _on_search_complete(self, results: List[DataEntry]):
        self.lbl_loading.grid_remove()
        self.btn_search.configure(state="normal")
        self.display_results(results)

    def _on_filter_changed(self, choice):
        self.perform_search()
        
    def display_results(self, results: List[DataEntry]):
        if self._batch_after_id:
            self.after_cancel(self._batch_after_id)
            self._batch_after_id = None

        # Clear existing
        for widget in self._result_widgets:
            try:
                widget.destroy()
            except: pass
        self._result_widgets = []
            
        if not results:
            lbl = ctk.CTkLabel(self.scroll_frame, text="No results found.", font=ctk.CTkFont(size=14, slant="italic"))
            lbl.grid(row=0, column=0, pady=20, sticky="ew")
            self._result_widgets.append(lbl)
            return

        display_limit = 100
        visible_results = results[:display_limit]
        
        self._render_batch(visible_results, 0, len(results) > display_limit, len(results))

    def _render_batch(self, results: List[DataEntry], start_index: int, show_more: bool, total_count: int):
        batch_size = 10 
        end_index = min(start_index + batch_size, len(results))
        
        for i in range(start_index, end_index):
            entry = results[i]
            card = DataCard(
                self.scroll_frame,
                entry=entry,
                on_view_detail=self.show_detail,
                on_select_toggle=self.handle_select_toggle
            )
            card.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
            self._result_widgets.append(card)
            
            # Explicitly propagate scroll events for macOS safely
            self._bind_scroll_recursive(card, self._on_mousewheel_results)
            
            if entry in self.selected_entries:
                card.checkbox_var.set(True)
        
        if end_index < len(results):
            self._batch_after_id = self.after(10, lambda: self._render_batch(results, end_index, show_more, total_count))
        else:
            if show_more:
                lbl = ctk.CTkLabel(
                    self.scroll_frame,
                    text=f"...and {total_count - len(results)} more results.",
                    font=ctk.CTkFont(size=12, slant="italic")
                )
                lbl.grid(row=len(results), column=0, pady=10, sticky="ew")
                self._result_widgets.append(lbl)
                self._bind_scroll_recursive(lbl, self._on_mousewheel_results)
            
            self._batch_after_id = None
            # Force update scrollregion/scrollbar
            self.scroll_frame.update_idletasks()

    def handle_select_toggle(self, entry: DataEntry, is_selected: bool):
        if is_selected:
            if entry not in self.selected_entries:
                self.selected_entries.append(entry)
        else:
            if entry in self.selected_entries:
                self.selected_entries.remove(entry)
                
        self.update_export_button()
        
    def update_export_button(self):
        count = len(self.selected_entries)
        if count > 0:
            self.btn_export.configure(
                state="normal",
                text=f"Export Selected ({count})",
                fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"]
            )
        else:
            self.btn_export.configure(
                state="disabled",
                text="Export Selected (0)",
                fg_color="transparent"
            )
            
    def show_detail(self, entry: DataEntry):
        self.detail_textbox.configure(state="normal")
        self.detail_textbox.delete("0.0", "end")
        self.detail_textbox.insert("0.0", entry.content_markdown)
        self.detail_textbox.configure(state="disabled")
        self.detail_textbox.see("0.0")

    def export_selected(self):
        if not self.selected_entries:
            return
            
        from core.export import export_entries_to_markdown
        from tkinter import messagebox
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            title="Export Selected Data"
        )
        
        if file_path:
            success = export_entries_to_markdown(self.selected_entries, file_path)
            if success:
                messagebox.showinfo("Export Successful", f"Successfully exported {len(self.selected_entries)} items to\n{file_path}")
                self.selected_entries.clear()
                self.update_export_button()
                self.perform_search() 
            else:
                messagebox.showerror("Export Failed", "There was an error exporting the items. Check the logs.")

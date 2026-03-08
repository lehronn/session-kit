import customtkinter as ctk
from core.config import config_manager, ThemeConfig
from gui.localization import loc
from gui.views.settings_view import SettingsView

class SessionKitApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Session Kit")
        self.geometry(f"{1100}x{700}")
        self.minsize(800, 600)
        
        # Setup localization language up front
        loc.set_language(config_manager.config.language.value)

        # Determine theme
        self._apply_theme()
            
        # Build UI layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Session Kit", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.settings_button = ctk.CTkButton(self.sidebar_frame, text=loc.get("settings"), command=self.show_settings)
        self.settings_button.grid(row=1, column=0, padx=20, pady=10)
        
        # Main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.welcome_label = ctk.CTkLabel(self.main_frame, text=loc.get("welcome"), font=ctk.CTkFont(size=24))
        self.welcome_label.grid(row=0, column=0)

        # Settings View
        self.settings_view = SettingsView(self.main_frame, on_settings_changed=self.on_settings_changed)

    def _apply_theme(self):
        theme = config_manager.config.theme
        if theme == ThemeConfig.AUTO:
            ctk.set_appearance_mode("System")
        elif theme == ThemeConfig.LIGHT:
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

    def show_settings(self):
        self.welcome_label.grid_forget()
        self.settings_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def on_settings_changed(self):
        # Update localization language
        loc.set_language(config_manager.config.language.value)
        # Apply theme
        self._apply_theme()
        # Update texts
        self.settings_button.configure(text=loc.get("settings"))
        self.welcome_label.configure(text=loc.get("welcome"))
        self.settings_view.update_texts()

import customtkinter as ctk
from core.config import config_manager
from core.models import ThemeConfig, AppLanguage, RulesetVersion
from gui.localization import loc

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, on_settings_changed=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_settings_changed = on_settings_changed
        
        self.grid_columnconfigure(1, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(self, text=loc.get("settings"), font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        
        # Language Selection
        self.lang_label = ctk.CTkLabel(self, text=loc.get("language"))
        self.lang_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.lang_var = ctk.StringVar(value=config_manager.config.language.value)
        self.lang_dropdown = ctk.CTkOptionMenu(
            self, 
            values=[AppLanguage.EN.value, AppLanguage.PL.value],
            variable=self.lang_var,
            command=self._on_change
        )
        self.lang_dropdown.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        
        # Theme Selection
        self.theme_label = ctk.CTkLabel(self, text=loc.get("theme"))
        self.theme_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        self.theme_var = ctk.StringVar(value=config_manager.config.theme.value)
        self.theme_dropdown = ctk.CTkOptionMenu(
            self,
            values=[ThemeConfig.LIGHT.value, ThemeConfig.DARK.value, ThemeConfig.AUTO.value],
            variable=self.theme_var,
            command=self._on_change
        )
        self.theme_dropdown.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        
        # Ruleset Selection
        self.ruleset_label = ctk.CTkLabel(self, text=loc.get("ruleset"))
        self.ruleset_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.ruleset_var = ctk.StringVar(value=config_manager.config.active_ruleset.value)
        self.ruleset_dropdown = ctk.CTkOptionMenu(
            self,
            values=[RulesetVersion.DND50E.value, RulesetVersion.DND55E.value, RulesetVersion.DND50E_SDR.value, RulesetVersion.DND55E_SDR.value],
            variable=self.ruleset_var,
            command=self._on_change
        )
        self.ruleset_dropdown.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

    def _on_change(self, value):
        config_manager.update_config(
            language=AppLanguage(self.lang_var.get()),
            theme=ThemeConfig(self.theme_var.get()),
            active_ruleset=RulesetVersion(self.ruleset_var.get())
        )
        if self.on_settings_changed:
            self.on_settings_changed()

    def update_texts(self):
        self.title_label.configure(text=loc.get("settings"))
        self.lang_label.configure(text=loc.get("language"))
        self.theme_label.configure(text=loc.get("theme"))
        self.ruleset_label.configure(text=loc.get("ruleset"))

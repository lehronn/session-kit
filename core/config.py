import json
import os
from .models import AppConfigModel, AppLanguage, RulesetVersion, ThemeConfig

CONFIG_FILE = "config.json"

class AppConfigManager:
    def __init__(self):
        self.config = AppConfigModel()
        self.load_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config.language = AppLanguage(data.get("language", AppLanguage.EN.value))
                    self.config.active_ruleset = RulesetVersion(data.get("active_ruleset", RulesetVersion.DND55E.value))
                    self.config.theme = ThemeConfig(data.get("theme", ThemeConfig.AUTO.value))
            except Exception as e:
                print(f"Failed to load config, using defaults: {e}")
                self.save_config()
        else:
            self.save_config()

    def save_config(self):
        data = {
            "language": self.config.language.value,
            "active_ruleset": self.config.active_ruleset.value,
            "theme": self.config.theme.value
        }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def update_config(self, language=None, active_ruleset=None, theme=None):
        if language:
            self.config.language = language
        if active_ruleset:
            self.config.active_ruleset = active_ruleset
        if theme:
            self.config.theme = theme
        self.save_config()

# Global instance for easy access
config_manager = AppConfigManager()
from core.models import AppLanguage

_TRANSLATIONS = {
    "en": {
        "settings": "Settings",
        "language": "Language",
        "theme": "Theme",
        "ruleset": "Ruleset Version",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "theme_auto": "Auto",
        "lang_en": "English",
        "lang_pl": "Polish",
        "save": "Save Settings",
        "welcome": "Welcome to Session Kit",
    },
    "pl": {
        "settings": "Ustawienia",
        "language": "Język",
        "theme": "Motyw",
        "ruleset": "Zbiór Zasad",
        "theme_light": "Jasny",
        "theme_dark": "Ciemny",
        "theme_auto": "Automatyczny",
        "lang_en": "Angielski",
        "lang_pl": "Polski",
        "save": "Zapisz ustawienia",
        "welcome": "Witamy w Session Kit",
    }
}

class LocalizationManager:
    def __init__(self):
        self.current_lang = AppLanguage.EN.value

    def set_language(self, lang: str):
        self.current_lang = lang

    def get(self, key: str) -> str:
        lang_dict = _TRANSLATIONS.get(self.current_lang, _TRANSLATIONS["en"])
        return lang_dict.get(key, f"[{key}]")

loc = LocalizationManager()

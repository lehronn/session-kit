from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import uuid
from enum import Enum

class DataEntryType(str, Enum):
    SPELL = "SPELL"
    MONSTER = "MONSTER"
    ITEM = "ITEM"
    CLASS = "CLASS"
    FEATURE = "FEATURE"
    RACE = "RACE"
    BACKGROUND = "BACKGROUND"

class RulesetVersion(str, Enum):
    DND50E = "dnd50e"
    DND55E = "dnd55e"
    DND50E_SDR = "dnd50e_sdr"
    DND55E_SDR = "dnd55e_sdr"
    
class ThemeConfig(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"
    
class AppLanguage(str, Enum):
    EN = "en"
    PL = "pl"

class EncounterDifficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    DEADLY = "DEADLY"

@dataclass
class DataEntry:
    id: str
    name: str
    type: DataEntryType
    source: str
    content_markdown: str

@dataclass
class Character:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    ruleset_version: RulesetVersion = RulesetVersion.DND55E
    race: str = ""
    background: str = ""
    classes: List[Tuple[str, int]] = field(default_factory=list)
    abilities: Dict[str, int] = field(default_factory=lambda: {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10})
    hp_max: int = 0
    hp_current: int = 0
    hp_temp: int = 0
    ac: int = 10
    speed: int = 30
    initiative_bonus: int = 0
    equipment: List[Dict] = field(default_factory=list)
    spells_known: List[str] = field(default_factory=list)
    spell_slots: Dict[int, int] = field(default_factory=dict)

@dataclass
class Encounter:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    difficulty: EncounterDifficulty = EncounterDifficulty.MEDIUM
    target_xp_budget: int = 0
    actual_xp_spent: int = 0
    monsters: List[Dict] = field(default_factory=list)
    loot: Dict = field(default_factory=dict)

@dataclass
class AppConfigModel:
    language: AppLanguage = AppLanguage.EN
    active_ruleset: RulesetVersion = RulesetVersion.DND55E
    theme: ThemeConfig = ThemeConfig.AUTO
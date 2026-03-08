from abc import ABC, abstractmethod
from typing import Dict, List, Any
from .models import Character, Encounter, RulesetVersion

class DnDRules(ABC):
    
    @property
    @abstractmethod
    def version(self) -> RulesetVersion:
        pass
        
    @abstractmethod
    def calculate_hp(self, char: Character) -> int:
        """Calculate max Hit Points based on class, con, and level."""
        pass
        
    @abstractmethod
    def calculate_ac(self, char: Character) -> int:
        """Calculate Armor Class based on equipment, dex, and features."""
        pass
        
    @abstractmethod
    def calculate_encounter_difficulty(self, party_levels: List[int], monsters_xp: List[int]) -> Encounter:
        """Calculates encounter budget based on ruleset."""
        pass

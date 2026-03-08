from typing import List
from .models import Character, Encounter, RulesetVersion
from .rules import DnDRules

class Rules_dnd50e(DnDRules):
    
    @property
    def version(self) -> RulesetVersion:
        return RulesetVersion.DND50E
        
    def calculate_hp(self, char: Character) -> int:
        # TODO: Implement 2014 specific HP math
        return char.hp_max
        
    def calculate_ac(self, char: Character) -> int:
        # TODO: Implement 2014 specific AC math
        return char.ac
        
    def calculate_encounter_difficulty(self, party_levels: List[int], monsters_xp: List[int]) -> Encounter:
        # TODO: Implement 2014 CR to XP math rules
        return Encounter()

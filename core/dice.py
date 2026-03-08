import random
from typing import List, Tuple

class DiceRoller:
    
    @staticmethod
    def roll(num_dice: int, sides: int, modifier: int = 0) -> Tuple[int, List[int]]:
        """Rolls a number of dice with given sides and adds a modifier. Returns total and individual rolls."""
        if num_dice <= 0 or sides <= 0:
            return 0, []
            
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        total = sum(rolls) + modifier
        return total, rolls
        
    @staticmethod
    def roll_ability_score() -> int:
        """Rolls 4d6 and drops the lowest for stat generation."""
        _, rolls = DiceRoller.roll(4, 6)
        rolls.remove(min(rolls))
        return sum(rolls)
        
    @staticmethod
    def roll_d20(modifier: int = 0, advantage: bool = False, disadvantage: bool = False) -> Tuple[int, List[int]]:
        """Rolls a d20, handling advantage and disadvantage."""
        if advantage and disadvantage:
            advantage = disadvantage = False
            
        if advantage or disadvantage:
            _, rolls = DiceRoller.roll(2, 20)
            chosen = max(rolls) if advantage else min(rolls)
            return chosen + modifier, rolls
            
        return DiceRoller.roll(1, 20, modifier)

# Data Model: Core Application

## Entities

### `DataEntry`
Represents any searchable D&D resource (Monster, Spell, Item, Class, Feature).
- `id` (UUID or String): Unique identifier.
- `name` (String): Polish or English localized name.
- `type` (Enum): `SPELL`, `MONSTER`, `ITEM`, `CLASS`, `FEATURE`, `RACE`, `BACKGROUND`.
- `source` (String): e.g., "PHB 2014", "D&D 5.5e 2024".
- `content_markdown` (String): The full description text formatted in Markdown.

### `Character`
Represents a player's character sheet.
- `id` (UUID)
- `name` (String)
- `ruleset_version` (Enum): `dnd50e`, `dnd55e`, `dnd50e_sdr`, `dnd55e_sdr`
- `race` (String)
- `background` (String)
- `classes` (List[tuple(String, int)]): Class names and their level.
- `abilities` (Dict[String, int]): STR, DEX, CON, INT, WIS, CHA scores.
- `hp_max` (int), `hp_current` (int), `hp_temp` (int)
- `ac` (int), `speed` (int), `initiative_bonus` (int)
- `equipment` (List[Dict]): Items carried and equipped.
- `spells_known` (List[String]), `spell_slots` (Dict[int, int])

### `Encounter`
Represents a generated combat scenario.
- `id` (UUID)
- `difficulty` (Enum): `EASY`, `MEDIUM`, `HARD`, `DEADLY`
- `target_xp_budget` (int)
- `actual_xp_spent` (int)
- `monsters` (List[Dict]): List of monster structs including UUID, current HP, and initiative roll.
- `loot` (Dict): Generated gold and items.

### `AppConfig`
User preferences saved locally.
- `language` (Enum): `pl`, `en`
- `active_ruleset` (Enum): `dnd50e`, `dnd55e`, `dnd50e_sdr`, `dnd55e_sdr`
- `theme` (Enum): `light`, `dark`, `auto`

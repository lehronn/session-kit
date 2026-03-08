# Feature Specification: Core Application

**Feature Branch**: `001-core-app`  
**Created**: 2026-03-08  
**Status**: Draft  
**Input**: User description: "Session Kit Core Application including character creator, encounter generator and search functionality."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Desktop App Installation and Setup (Priority: P1)

As a D&D player/Dungeon Master, I want to install a lightweight desktop application on my OS (macOS, Windows, or Linux) and choose my preferred language and rule sets (5e 2014 or 5.5e 2024) so I can start managing my session.

**Why this priority**: Without core setup, source data management, and a functional GUI, no other features can work.

**Independent Test**: Can be fully tested by running the application, selecting English or Polish, and configuring the active D&D source (e.g., D&D 5.5e).

**Acceptance Scenarios**:
1. **Given** the app is launched for the first time, **When** I click settings, **Then** I am prompted to select my GUI language (Polish or English) and rule system version.
2. **Given** I am in the Source Manager, **When** I select "D&D 5.5e", **Then** the application context switches to only use 5.5e data for search and interactions.

---

### User Story 2 - Search Engine for D&D Data (Priority: P1)

As a user, I want to search and filter through D&D resources (spells, monsters, items, classes, etc.) with clear visual indicators of their types, so I can quickly reference rules during a game.

**Why this priority**: Quick referencing of data is the primary real-time use case during actual D&D sessions.

**Independent Test**: Can be tested by searching for a specific spell or monster, applying filters, and verifying the result matches the data files.

**Acceptance Scenarios**:
1. **Given** the search interface, **When** I type "Fireball" and filter by "Spells", **Then** I see the Fireball spell with a visual "Spell" indicator.
2. **Given** a list of search results, **When** I select multiple items and click "Export to Markdown", **Then** a single valid `.md` file with all selected items' details is generated.

---

### User Story 3 - Character Creator and Manager (Priority: P2)

As a player, I want to create and manage character sheets according to either 5.0e or 5.5e rules, so I can track my stats, HP, equipment, and spells digitally.

**Why this priority**: Essential for players, but complex. Should be built after the data search engine is functional.

**Independent Test**: Can be tested by generating a new Level 1 character, choosing a race, class, background, and verifying HP and AC are calculated correctly based on the chosen ruleset.

**Acceptance Scenarios**:
1. **Given** the character creation flow, **When** I select D&D 5.5e rules, **Then** the character is constrained by the 2024 updated rules for classes and backgrounds.
2. **Given** an existing character, **When** I click "Level Up", **Then** I am prompted to add new HP, features, and spells.
3. **Given** a character detail view, **When** I choose "Export to Markdown", **Then** a markdown version of the character sheet is copied to my clipboard.

---

### User Story 4 - Encounter Generator (Priority: P2)

As a Dungeon Master, I want to generate balanced combat encounters based on party size, average level, and desired difficulty, so I can seamlessly run combat in my game.

**Why this priority**: Highly valuable for DMs, but relies heavily on the monster database and rule interpretations.

**Independent Test**: Can be tested by inputting a party of 4 level 5 characters and selecting "Boss" combat on "Hard" difficulty, and checking if the resulting enemy total CR/EXP matches budget rules.

**Acceptance Scenarios**:
1. **Given** the encounter generator, **When** I specify an environment (e.g., "Forest") and "Swarm" type, **Then** the app only generates monsters native to the Forest in large numbers.
2. **Given** a generated encounter, **When** I click "Roll Initiative", **Then** all enemies receive a randomized initiative score, and randomized loot is generated for the encounter.

---

### User Story 5 - Integrated Dice Roller (Priority: P3)

As a player or Dungeon Master, I want an integrated dice rolling tool directly accessible via a dedicated button for quick standalone rolls (d2, d3, d6, d8, d10, d12, d20, d100), as well as contextual rolls directly from the character sheet and encounter views.

**Why this priority**: Greatly enhances Quality of Life but is not strictly necessary for the core logic of managing data.

**Independent Test**: Can be tested by rolling a d20 skill check from the character sheet or generating ability scores via standard dice arrays.

**Acceptance Scenarios**:
1. **Given** the character creator, **When** I am generating ability scores, **Then** I have the option to trigger a standard 4d6 (drop lowest) roll for STR, DEX, CON, INT, WIS, and CHA.
2. **Given** the character manager, **When** I click on a weapon or spell damage entry, **Then** the app automatically rolls the correct damage dice and modifier.
3. **Given** the character manager, **When** I click on an ability saving throw, **Then** the app rolls a d20 plus the saving throw modifier.

### Edge Cases

- What happens when a requested encounter biome has no monsters fitting the required CR budget? System will fallback to any monster of the appropriate CR and display a warning to the user.
- How does the system handle selecting a source (e.g., D&D 5.5e Polish) that is missing from the data folder? The system will alert the user to generate/download the data and fallback to the default English source.
- What happens if the calculated encounter budget is too low for even the weakest monster? The system will generate the encounter with a single 0 CR or 1/8 CR monster and warn the user.

### Functional Requirements

- **FR-001**: System MUST function as a standalone desktop GUI application natively on macOS, Windows, and Linux.
- **FR-002**: System MUST allow users to select and manage their actively used data sources (e.g., 5.0e vs 5.5e).
- **FR-003**: System MUST support a multi-language GUI, starting with English and Polish. Polish terminology MUST adhere to Rebel publishing standards.
- **FR-004**: System MUST provide a fast, categorizable search interface for all D&D data types (spells, items, classes, monsters, etc.) with clear visual type indicators.
- **FR-005**: System MUST allow single and multi-selection of data entries for exporting to a single Markdown file or copying to clipboard.
- **FR-006**: System MUST implement a Character Creator adhering to chosen 5.0e or 5.5e rules.
- **FR-007**: System MUST provide a Character Manager to view, level up, and edit stats/equipment/spells of created characters.
- **FR-008**: System MUST implement an Encounter Generator calculating CR/EXP budgets dynamically based on user input (party size, level, difficulty).
- **FR-009**: System MUST support 4 encounter archetypes: Boss, Gang, Swarm, and Random.
- **FR-010**: System MUST be able to roll initiative for enemies and generate randomized loot based on the encounter.
- **FR-011**: System MUST filter encounter generation by biome/location based on data. If no monsters match the biome and CR requirements, the system MUST fallback to any monster of the appropriate CR and warn the user.
- **FR-012**: System MUST include a global dice roller accessible via a dedicated dedicated UI button allowing manual quick rolls of standard dice (d2, d3, d6, d8, d10, d12, d20, d100).
- **FR-013**: System MUST provide 1-click contextual rolls from the Character Sheet for Ability Checks, Saving Throws, Initiatives, Attacks (Hit), Damage (Weapon/Spell), and Hit Dice (HP generation/recovery).
- **FR-014**: System MUST provide an automated 4d6 drop-lowest generation tool for the Character Creator attribute rolling.

### Key Entities

- **Source Configuration**: User's chosen rule set (e.g., dnd50e/dnd55e or their SDR variants) and GUI language.
- **Data Entry**: Generic wrapper for any searchable resource (Spell, Item, Monster, Feature) containing title, type, and markdown description.
- **Character**: Player character data containing stats, HP, AC, race, class, background, equipment, and spells, linked to a specific ruleset.
- **Encounter**: A generated combat scenario containing a list of enemy stats, calculated total XP, initiative rolls, and loot.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Application can be built into native installers (.dmg, .exe, .deb, .rpm) using a build script.
- **SC-002**: Users can search for any record in the database and receive results in under 500 milliseconds.
- **SC-003**: A user can export multiple selected data items into a combined Markdown file successfully.
- **SC-004**: The Encounter Generator always outputs an encounter whose total XP budget falls within 10% of the target mathematical threshold for the chosen difficulty.

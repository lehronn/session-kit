# Tasks: Core Application

**Input**: Design documents from `/specs/001-core-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure.

- [x] T001 Initialize Python project structure and virtual environment
- [x] T002 [P] Install `customtkinter` and `pytest` dependencies (skipped due to environment restrictions)
- [x] T003 Create `tests/` directory structure (`unit/`, `integration/`)
- [x] T004 Create `scripts/build.sh` stub script
- [x] T005 Create data model classes (DataEntry, Character, Encounter, AppConfig) in `core/models.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [x] T006 Implement base `AppConfig` manager in `core/config.py` for localized language/theme/ruleset
- [x] T007 [P] Create base `DnDRules` strategy interface in `core/rules.py`
- [x] T008 Implement `Rules_dnd50e` and `Rules_dnd55e` stubs extending `DnDRules` in `core/rules_dnd50e.py` and `core/rules_dnd55e.py`
- [x] T009 [P] Initialize base CustomTkinter App window in `gui/app.py`
- [x] T010 [P] Implement global Dice Roller utility in `core/dice.py` supporting `d2, d3, d4, d6, d8, d10, d12, d20, d100`

---

## Phase 3: User Story 1 - Desktop App Installation and Setup (Priority: P1) 🎯 MVP

**Goal**: As a D&D player/DM, I want to install a lightweight application and choose my language and rule sets (50e vs 55e) so I can start managing my session.

**Independent Test**: Can be fully tested by running the app, selecting English/Polish, and configuring the active D&D source.

### Implementation for User Story 1

- [x] T011 [US1] Build initial Settings UI View in `gui/views/settings_view.py`
- [x] T012 [US1] Wire Settings UI to `AppConfig` manager allowing language, theme (`light`, `dark`, `auto`), and active ruleset selection
- [x] T013 [P] [US1] Implement Polish vs English simple localization dictionary system in `gui/localization.py`
- [x] T014 [US1] Complete the `scripts/build.sh` script to invoke PyInstaller to package into OS-native installers (.dmg/.exe/.deb)

---

## Phase 4: User Story 2 - Search Engine for D&D Data (Priority: P1)

**Goal**: Search and filter through D&D resources with clear visual indicators of their types.

**Independent Test**: Search for "Fireball", filter by "Spells", and export selected items to markdown.

### Implementation for User Story 2

- [ ] T015 [P] [US2] Create data parser in `data/loader.py` to ingest CSV/MD files into `DataEntry` models
- [ ] T016 [US2] Implement fast, in-memory `data/search.py` system with filtering/sorting based on active ruleset
- [ ] T017 [US2] Build Search UI View in `gui/views/search_view.py` with search bar and filter dropdowns
- [ ] T018 [US2] Build `gui/components/data_card.py` to visually represent a `DataEntry` (Spell/Monster/etc.)
- [ ] T019 [US2] Implement markdown export logic combining multiple `DataEntry` contents in `core/export.py`
- [ ] T020 [US2] Wire UI multiselect export button to `core/export.py`

---

## Phase 5: User Story 5 - Integrated Dice Roller (Priority: P3)

**Goal**: Integrated dice rolling accessible via a dedicated button for quick standalone rolls.

**Independent Test**: Roll a d20 from the dedicated button in the GUI.

### Implementation for User Story 5

- [ ] T021 [US5] Implement Quick Dice Roller UI widget in `gui/components/dice_widget.py`
- [ ] T022 [US5] Wire Quick Dice Roller buttons (d2, d3, d6, d8, d10, d12, d20, d100) to `core/dice.py`
- [ ] T023 [US5] Inject Quick Dice Roller into the main `gui/app.py` layout as a floating or side panel

---

## Phase 6: User Story 3 - Character Creator and Manager (Priority: P2)

**Goal**: Create and manage character sheets according to dnd50e or dnd55e rules.

**Independent Test**: Generate a new Level 1 character and verify HP and AC are calculated correctly based on rules.

### Implementation for User Story 3

- [ ] T024 [P] [US3] Finalize `Rules_dnd50e` and `Rules_dnd55e` stat/HP calculation math in their respective modules
- [ ] T025 [P] [US3] Implement `core/character_manager.py` to handle CRUD operations for `Character` entities (saving to JSON/SQLite)
- [ ] T026 [US3] Build Character List/Manager View in `gui/views/character_list_view.py`
- [ ] T027 [US3] Build Character Creator View in `gui/views/character_creator_view.py` with 4d6-drop-lowest attribute generation tool leveraging `core/dice.py`
- [ ] T028 [US3] Build Character Detail View in `gui/views/character_detail_view.py`
- [ ] T029 [US3] Implement contextual 1-click rolls (Ability Checks, Saves, Attacks, Damage) from the Character Detail View delegating to `core/dice.py`

---

## Phase 7: User Story 4 - Encounter Generator (Priority: P2)

**Goal**: Generate balanced combat encounters based on party size, level, and difficulty.

**Independent Test**: Input party of 4 lv5 characters, select "Boss" on "Hard", and check if CR/EXP bounds are respected.

### Implementation for User Story 4

- [ ] T030 [P] [US4] Implement XP/CR math calculator in `core/encounter.py` based on active ruleset
- [ ] T031 [US4] Implement Boss, Gang, Swarm, and Random encounter generation logic filtering by biome
- [ ] T032 [US4] Build Encounter Generator View in `gui/views/encounter_view.py`
- [ ] T033 [US4] Build Generated Encounter Details View in `gui/views/encounter_detail_view.py`
- [ ] T034 [US4] Add "Roll Initiative" button to Encounter Details delegating to `core/dice.py` setting enemy initiatives
- [ ] T035 [US4] Add randomized loot generation per encounter

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [ ] T036 Write unit tests for `core/rules_dnd50e` and `core/rules_dnd55e`
- [ ] T037 Write unit tests for `core/search` speed constraints (<500ms)
- [ ] T038 Write unit tests for `core/encounter` math logic validating 10% target thresholds
- [ ] T039 Clean up UI styling and dark/light modes consistency
- [ ] T040 Final documentation and README updates

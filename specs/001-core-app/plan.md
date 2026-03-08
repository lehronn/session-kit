# Implementation Plan: Core Application

**Branch**: `001-core-app` | **Date**: 2026-03-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-core-app/spec.md`

## Summary

Build the Session Kit desktop application incorporating a dynamic data search engine, character creator/manager, and encounter generator using Python with a modern, lightweight GUI, optimized for low dependencies and cross-platform native packaging.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: CustomTkinter (for lightweight, modern GUI), PyInstaller/Briefcase (for packaging)
**Storage**: Local JSON/CSV files for reference data; SQLite/JSON for user characters and settings.
**Testing**: pytest
**Target Platform**: macOS, Windows, Linux Desktop
**Project Type**: Desktop Application
**Performance Goals**: <500ms search latency across all data
**Constraints**: Minimal external dependencies; single build script for cross-platform installers.
**Scale/Scope**: Local offline application managing thousands of D&D entities.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Test-First (Constitution Principle III)**: All core logic (search filtering, CR math, hit point calculation) must be covered by unit tests before GUI integration.
- **Simplicity**: Favor standard Python libraries where possible.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-app/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
```

### Source Code (repository root)

```text
session_kit/
├── main.py            # Entry point
├── core/              # Domain logic (rules, math, models)
│   ├── rules_dnd50e.py
│   ├── rules_dnd55e.py
│   ├── encounter.py
│   └── dice.py        # Dice roller and standard roll logic
├── data/              # Data access layer
│   ├── loader.py
│   └── search.py
├── gui/               # CustomTkinter interface
│   ├── app.py
│   ├── views/
│   └── components/
└── scripts/           # Build and dev scripts
    └── build.sh
tests/
├── unit/
└── integration/
```

**Structure Decision**: A modular monolith isolating core D&D logic from the GUI. This fulfills the requirement for the UI to be lightweight and replaceable while ensuring the complex rules (5.0e vs 5.5e) are fully testable in isolation.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Custom cross-platform build script | User specifically requested a `.sh` script creating `.dmg`, `.exe`, `.deb`, `.rpm`. | Standard `pip install` or single-platform binaries do not fulfill the user's native installer requirement. |

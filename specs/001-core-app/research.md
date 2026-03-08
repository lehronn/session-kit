# Research: Core Application Phase 0

## 1. GUI Framework Selection
- **Decision**: `CustomTkinter`
- **Rationale**: The user requested a "lightweight, modern GUI", written in Python, that "limits external dependencies to absolute minimum." `CustomTkinter` is built directly on top of Python's built-in `tkinter`, meaning it does not require massive C++ binaries like Qt (`PyQt6`/`PySide6`). It provides a very modern, dark-mode compatible, flat UI design out of the box that fulfills the visual requirements while being incredibly lightweight.
- **Alternatives considered**: 
  - `PySide6`/`PyQt6`: Extremely feature-rich but heavily bloats the application size (often 100MB+ just for the framework).
  - `Flet`: Uses Flutter under the hood, requiring downloading the Flutter engine. Heavy.
  - `Tkinter` (vanilla): Extremely lightweight (0 dependencies) but looks very archaic and requires immense manual styling to look "modern".

## 2. Packaging System Generation
- **Decision**: `PyInstaller` combined with OS-native tools in a build script.
- **Rationale**: The user wants a `.sh` script that generates `.dmg`, `.exe`, `.deb`, and `.rpm`. A bash script (`build.sh`) will orchestrate `PyInstaller` to create the standalone executable. To generate the installers, the script will use tools like `appdmg` (macOS), `Inno Setup` (Windows, via wine or native if on Windows), and `fpm` (Linux) to wrap the PyInstaller binary. *Note ensuring true cross-compilation of Windows .exe from Mac/Linux is prone to errors, so the script might require running on the target OS or Docker for full coverage.*
- **Alternatives considered**:
  - `Briefcase` (BeeWare): Good native installer support, but often abstracts too much away and breaks with non-standard project structures.
  - `Nuitka`: Compiles to C++ first for performance, but packaging into native OS installers is still a manual post-step.

## 3. Data Storage and Search Performance
- **Decision**: In-memory inverted index or structured dictionary built on startup.
- **Rationale**: The `/data` folder contains CSV/Markdown files. For sub-500ms search latency across thousands of entries, parsing them at startup into an optimized Python dictionary/list structure and searching in-memory is fastest.
- **Alternatives considered**:
  - `SQLite` database: Good for complex queries, but overkill for read-mostly D&D data that easily fits in RAM (~10-50MB max).

## 4. Rule Version Flexibility (dnd50e vs dnd55e vs sdr)
- **Decision**: Strategy Pattern for character/encounter logic.
- **Rationale**: By defining a common interface `DnDRules`, we can implement strategy variants for `Rules_dnd50e`, `Rules_dnd55e`, and their SDR variations. The GUI and Search will inject the ruleset currently selected by the user.

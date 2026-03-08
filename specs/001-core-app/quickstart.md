# Quickstart: Core Application

Welcome to the Session Kit development environment.

## Prerequisites
- Python 3.11 or higher
- `uv` (recommended for fast package management) or `pip`

## Setup

1. **Clone and Setup Virtual Environment:**
   ```bash
   git clone <repo-url> session-kit
   cd session-kit
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or using uv:
   # uv pip install -r requirements.txt
   ```
   *Note: Dependencies will include `customtkinter`, `pytest`, etc.*

3. **Run the Application locally:**
   ```bash
   python main.py
   ```

## Running Tests
To verify core rules and logic:
```bash
pytest tests/
```

## Building the App
To package the app using the build script:
```bash
./scripts/build.sh
```
This script will eventually trigger PyInstaller to generate native wrappers for your OS.

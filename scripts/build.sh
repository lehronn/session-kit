#!/bin/bash
set -e

echo "Starting Session Kit Build Process..."

# Ensure we're in the right directory
cd "$(dirname "$0")/.."

echo "Installing pyinstaller if not present..."
pip install pyinstaller || uv pip install pyinstaller || true

echo "Running PyInstaller..."
# We use --collect-all for customtkinter to bundle its assets properly.
# We include core, gui, and data using --add-data, which will handle the cross-platform path separators (PyInstaller handles ':' on Mac/Linux and ';' on Windows).
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* || "$OSTYPE" == "win32"* ]]; then
    SEP=";"
else
    SEP=":"
fi

pyinstaller --noconfirm --onedir --windowed --name "SessionKit" \
    --collect-all customtkinter \
    --add-data "core${SEP}core" \
    --add-data "gui${SEP}gui" \
    --add-data "data${SEP}data" \
    "main.py"

echo "Build complete. Check the 'dist' directory."
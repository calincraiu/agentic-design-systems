#!/bin/bash
# Starts the course app. Double-click this file. Close the window to stop the app.
# The first time, macOS may block it: right-click it, choose Open, then Open again.
cd "$(dirname "$0")" || exit 1
export PATH="$HOME/.local/bin:$PATH"
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv, the program that runs Python for the course. This happens once."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
echo "Starting the course app. The first time takes a minute."
uv run course

#!/bin/bash

# Navigate to the project directory (where this script is located)
cd "$(dirname "$0")"

# Check if the virtual environment exists
if [ -d ".venv" ]; then
    # Activate the virtual environment
    source .venv/bin/activate
else
    echo "Error: Virtual environment directory '.venv' not found."
    echo "Please create it first (e.g., python3 -m venv .venv) and install dependencies."
    exit 1
fi

# Run the application
# Using python (which should be the venv python after activation)
python filament_dryer_gui.py

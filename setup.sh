#!/bin/bash

# =============================================================================
# SmartGen Showcase - Local Setup Script
# Author: Sayad Md Bayezid Hosan
# =============================================================================

echo "Starting SmartGen Showcase setup..."

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed. Please install Python 3 to proceed."
    exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null
then
    echo "pip3 is not installed. Installing pip3..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install pip3. Please install it manually."
        exit 1
    fi
fi

echo "Installing SmartGen Showcase and its dependencies..."
# The "-e ." flag installs your local project in editable mode, 
# reading dependencies directly from your pyproject.toml or requirements.txt
pip3 install --user -e .

if [ $? -ne 0 ]; then
    echo "Error: Failed to install SmartGen Showcase. Please check the logs above."
    exit 1
fi

echo "============================================================"
echo "✔ SmartGen Showcase installed successfully!"
echo "============================================================"
echo "You can now use the 'smartgen-showcase' CLI command."
echo ""
echo "Common Commands:"
echo "  Initialize a new project:  smartgen-showcase init"
echo "  Build your showcase:       smartgen-showcase build"
echo "  Start a dev server:        smartgen-showcase serve"
echo ""

# Add ~/.local/bin to PATH if not already there (for current session)
if [[ ":$PATH:" != *":${HOME}/.local/bin:"* ]]; then
    echo "Notice: Adding ~/.local/bin to PATH for the current session."
    echo "Tip: You may want to add 'export PATH=\"\$HOME/.local/bin:\$PATH\"' to your ~/.bashrc or ~/.zshrc permanently."
    export PATH="${HOME}/.local/bin:$PATH"
fi

echo "Setup complete."
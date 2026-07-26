#!/bin/bash

# This script automates the setup and installation of SmartGen Docs.

echo "Starting SmartGen Docs setup..."

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3 to proceed."
    exit 1
fi

# Check for pip
if ! command -v pip3 &> /dev/null
then
    echo "pip3 is not installed. Installing pip3..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
    if [ $? -ne 0 ]; then
        echo "Failed to install pip3. Please install it manually."
        exit 1
    fi
fi

echo "Installing SmartGen Docs and its dependencies..."
pip3 install --user markdown2 Jinja2 PyYAML click watchdog fastapi uvicorn

if [ $? -ne 0 ]; then
    echo "Failed to install SmartGen Docs dependencies. Please check the error messages above."
    exit 1
fi

echo "SmartGen Docs installed successfully!"
echo "You can now use the 'smartgen-docs' command."
echo "To initialize a new project: smartgen-docs init"
echo "To build your documentation: smartgen-docs build"
echo "To start a development server: smartgen-docs serve"

# Add smartgen-docs to PATH if not already there (for current session)
# This might be needed if --user installation directory is not in PATH
if [[ ":$PATH:" != *":${HOME}/.local/bin:"* ]]; then
    echo "Adding ~/.local/bin to PATH for current session. You might want to add it permanently."
    export PATH="${HOME}/.local/bin:$PATH"
fi

echo "Setup complete."

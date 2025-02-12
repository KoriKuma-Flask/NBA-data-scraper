echo "Build complete." 

#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "🔹 Updating system and installing dependencies..."
sudo apt-get update && sudo apt-get install -y \
    wget \
    gnupg \
    xvfb \
    python3-tk \
    python3-dev


Xvfb :99 -screen 0 1920x1080x24 &
echo "Dependencies installed."

echo "🔹 Installing Google Chrome..."
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get update
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb



echo "🔹 Setting up Python environment"
pip install --no-cache-dir -r requirements.txt



echo "Setup complete!"
#!/bin/bash

# Install Chrome (adjust for your Linux distribution)

# Debian/Ubuntu example (most common):
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb  # Or latest .deb
sudo apt install ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb # Clean up the .deb file


# Install Python dependencies
pip install -r requirements.txt

# (Optional) Run your tests or other build commands here:
# sbase test my_test.py  # Example SeleniumBase test
# python your_script.py # Example run script

echo "Build complete."
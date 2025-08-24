#!/bin/bash

# Install system dependencies for Alex Voice Agent
echo "Installing system dependencies for Alex Voice Agent..."

# Update package list
sudo apt update

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Install Node.js and npm (for PM2)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PM2 globally
sudo npm install -g pm2

# Install audio dependencies (for voice processing)
sudo apt install -y portaudio19-dev python3-pyaudio

# Install other system dependencies
sudo apt install -y build-essential libssl-dev libffi-dev

# Create virtual environment (optional but recommended)
python3 -m venv alex-env
source alex-env/bin/activate

# Install Python dependencies
pip install -r requirements.txt

echo "Dependencies installed successfully!"
echo "Activate virtual environment with: source alex-env/bin/activate"
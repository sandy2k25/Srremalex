#!/bin/bash

# Alex Voice Agent VPS Setup Script
echo "Setting up Alex Voice Agent on VPS..."

# Create logs directory
mkdir -p logs

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install PM2 globally if not installed
if ! command -v pm2 &> /dev/null; then
    echo "Installing PM2..."
    npm install -g pm2
fi

# Create environment file
echo "Creating .env file..."
cat > .env << 'EOF'
LIVEKIT_API_KEY=APITMKfqYVjk79h
LIVEKIT_API_SECRET=gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA
LIVEKIT_URL=wss://sr-fa31r2za.livekit.cloud
GEMINI_API_KEY=your_gemini_api_key_here
PORT=5000
EOF

# Update ecosystem config with current directory
echo "Updating ecosystem config..."
CURRENT_DIR=$(pwd)
sed -i "s|/home/username/alex-voice-agent|$CURRENT_DIR|g" ecosystem.config.js

# Make scripts executable
chmod +x setup-vps.sh
chmod +x web_server.py
chmod +x agent.py

echo "Setup complete!"
echo "Next steps:"
echo "1. Update GEMINI_API_KEY in .env file"
echo "2. Run: pm2 start ecosystem.config.js"
echo "3. Run: pm2 startup"
echo "4. Run: pm2 save"
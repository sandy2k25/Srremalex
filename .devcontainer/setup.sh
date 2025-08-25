#!/bin/bash

echo "🚀 Setting up Alex Voice Agent development environment..."

# Make sure we're in the right directory
cd /workspaces/alex-voice-agent

# Update package lists
sudo apt-get update

# Install system dependencies for audio processing
echo "📦 Installing system dependencies..."
sudo apt-get install -y \
    portaudio19-dev \
    python3-dev \
    build-essential \
    ffmpeg \
    libffi-dev \
    libssl-dev

# Upgrade pip
python -m pip install --upgrade pip

# Install Python dependencies
echo "🐍 Installing Python dependencies..."

# Upgrade pip first
python -m pip install --upgrade pip

# Install from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing from requirements.txt..."
    python -m pip install -r requirements.txt --user
fi

# Install from pyproject.toml if available
if [ -f "pyproject.toml" ]; then
    echo "Installing from pyproject.toml..."
    python -m pip install -e . --user
fi

# Verify key packages are installed
echo "🔍 Verifying installations..."
python -c "import flask; print('✅ Flask installed')" 2>/dev/null || echo "⚠️ Flask not found"
python -c "import livekit; print('✅ LiveKit installed')" 2>/dev/null || echo "⚠️ LiveKit not found"

# Install Node.js dependencies if package.json exists
if [ -f "package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Check for API keys (Codespace secrets or .env file)
if [ -n "$GEMINI_API_KEY" ]; then
    echo "✅ GEMINI_API_KEY found in environment (from Codespace secrets)"
elif [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "🔧 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Remember to update .env with your actual API keys!"
elif [ -f ".env" ]; then
    echo "✅ .env file exists - using local environment file"
fi

# Make scripts executable
chmod +x *.sh 2>/dev/null || true

# Create logs directory for PM2 if it doesn't exist
mkdir -p logs

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Quick Start Commands for GitHub Codespaces:"
echo "  • Start Alex (EVERYTHING): python run-alex-codespace.py"
echo "  • Or start individually:"
echo "    - Web server: python web_server.py"
echo "    - Voice agent: python agent.py"
echo "  • Install additional deps: pip install <package>"
echo ""
echo "🔑 Environment setup:"
if [ -n "$GEMINI_API_KEY" ]; then
    echo "  ✅ GEMINI_API_KEY configured via Codespace secrets"
else
    echo "  • Update .env with your GEMINI_API_KEY"
fi
echo "  • Add other API keys as needed (OPENAI_API_KEY, etc.)"
echo ""
echo "🌐 Your app will be available at:"
echo "  • Web Interface: http://localhost:5000"
echo "  • View forwarded ports in the 'Ports' tab"
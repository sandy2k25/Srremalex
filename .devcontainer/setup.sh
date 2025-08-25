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
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Install from pyproject.toml if available
if [ -f "pyproject.toml" ]; then
    pip install -e .
fi

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
echo "🎯 Quick Start Commands:"
echo "  • Start web server: python web_server.py"
echo "  • Start voice agent: python -m livekit.agents.cli dev agent.py"
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
#!/bin/bash

echo "🚀 Starting Alex Voice Agent in GitHub Codespace..."
echo ""

# Check if we're in a Codespace
if [ "$CODESPACES" = "true" ]; then
    echo "✅ Running in GitHub Codespace environment"
else
    echo "⚠️  This script is optimized for GitHub Codespaces"
    echo "   It will work locally but some features may differ"
fi

echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file"
        echo "⚠️  Don't forget to add your GEMINI_API_KEY to .env"
    else
        echo "❌ .env.example not found"
    fi
else
    echo "✅ .env file exists"
fi

echo ""

# Check if dependencies are installed
echo "🔍 Checking Python dependencies..."
if python -c "import flask, livekit" 2>/dev/null; then
    echo "✅ Core dependencies installed"
else
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "🎯 Ready to start! Choose one option:"
echo ""
echo "   🚀 Start Everything (RECOMMENDED):"
echo "   python run-alex-codespace.py"
echo ""
echo "   📱 Or start individually:"
echo "   python web_server.py  (in one terminal)"
echo "   python agent.py       (in another terminal)"
echo ""
echo "   📱 Access your app:"
echo "   - Check the 'Ports' tab in VS Code"
echo "   - Web interface will be on port 5000"
echo ""

# If in Codespace, try to open the ports tab
if [ "$CODESPACES" = "true" ]; then
    echo "💡 Pro tip: Open the 'Ports' tab to see your running services"
fi

echo "Happy coding! 🎉"
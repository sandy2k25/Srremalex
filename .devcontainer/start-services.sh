#!/bin/bash

echo "🚀 Starting Alex Voice Agent Services in GitHub Codespaces"
echo ""

# Check if GEMINI_API_KEY is available
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY not found"
    echo "   Add it to your GitHub Codespace secrets"
    exit 1
fi

echo "✅ Environment configured"
echo ""

# Function to start web server
start_web_server() {
    echo "🌐 Starting Web Server..."
    python web_server.py
}

# Function to start agent
start_agent() {
    echo "🤖 Starting Alex Voice Agent..."
    # Use the codespace-optimized agent
    python .devcontainer/codespace-agent.py
}

# Check if argument provided
if [ "$1" = "web" ]; then
    start_web_server
elif [ "$1" = "agent" ]; then
    start_agent
elif [ "$1" = "both" ]; then
    echo "🔀 Starting both services..."
    echo "   Run 'bash .devcontainer/start-services.sh web' in one terminal"
    echo "   Run 'bash .devcontainer/start-services.sh agent' in another terminal"
else
    echo "Usage:"
    echo "  bash .devcontainer/start-services.sh web     # Start web server"
    echo "  bash .devcontainer/start-services.sh agent   # Start voice agent"
    echo "  bash .devcontainer/start-services.sh both    # Show instructions"
fi
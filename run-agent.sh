#!/bin/bash

# GitHub Codespaces-compatible agent launcher
echo "🤖 Starting Alex Voice Agent..."

# Make sure Gemini API key is available
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY not found in environment"
    echo "   Make sure it's added to your Codespace secrets"
    exit 1
else
    echo "✅ GEMINI_API_KEY found"
fi

# Set other environment variables
export LIVEKIT_API_KEY="APITMKfqYVjk79h"
export LIVEKIT_API_SECRET="gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA"
export LIVEKIT_URL="wss://sr-fa31r2za.livekit.cloud"

echo "🚀 Launching Alex Voice Agent..."
python agent.py
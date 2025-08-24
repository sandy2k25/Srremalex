#!/bin/bash

# Start Alex Voice Agent - VPS Compatible Script
echo "Starting Alex Voice Agent..."

# Check if virtual environment exists and activate it
if [ -d "alex-env" ]; then
    echo "Activating virtual environment..."
    source alex-env/bin/activate
fi

# Set Python path to current directory
export PYTHONPATH=".:$PYTHONPATH"

# Load environment variables
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    set -a
    source .env
    set +a
fi

# Check for required environment variables
if [ -z "$GEMINI_API_KEY" ] || [ "$GEMINI_API_KEY" = "your_gemini_api_key_here" ]; then
    echo "ERROR: GEMINI_API_KEY is not set or still has placeholder value"
    echo "Please update the .env file with your actual Gemini API key"
    exit 1
fi

# Start the agent using LiveKit CLI (development mode)
echo "Starting Alex voice agent..."
python -m livekit.agents.cli dev agent.py
#!/usr/bin/env python3
"""
GitHub Codespaces-optimized version of Alex Voice Agent
This version ensures environment variables are properly passed to child processes
"""

import os
import sys

def main():
    # Ensure GEMINI_API_KEY is available
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY not found in environment")
        print("   Make sure it's added to your Codespace secrets")
        sys.exit(1)
    
    print("✅ GEMINI_API_KEY found")
    
    # Set LiveKit environment variables
    os.environ.setdefault('LIVEKIT_API_KEY', 'APITMKfqYVjk79h')
    os.environ.setdefault('LIVEKIT_API_SECRET', 'gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA')
    os.environ.setdefault('LIVEKIT_URL', 'wss://sr-fa31r2za.livekit.cloud')
    
    # Import and run the agent
    sys.path.insert(0, '.')
    
    print("🚀 Starting Alex Voice Agent for GitHub Codespaces...")
    
    # Import the agent module
    import agent
    
    # Run the agent with proper environment handling
    from livekit import agents
    
    if __name__ == "__main__":
        agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=agent.entrypoint))

if __name__ == "__main__":
    main()
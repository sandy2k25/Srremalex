#!/usr/bin/env python3
"""
Single-file launcher for Alex Voice Agent in GitHub Codespaces
Run with: python run-alex-codespace.py
"""

import os
import sys
import time
import signal
import threading
import subprocess
from threading import Event

class AlexCodespaceLauncher:
    def __init__(self):
        self.stop_event = Event()
        self.web_process = None
        self.agent_process = None
        
    def check_environment(self):
        """Check if all required environment variables are available"""
        print("🔍 Checking environment...")
        
        # Check Gemini API key
        if not os.getenv('GEMINI_API_KEY'):
            print("❌ GEMINI_API_KEY not found in environment")
            print("   Make sure it's added to your GitHub Codespace secrets")
            return False
            
        print("✅ GEMINI_API_KEY found")
        
        # Set LiveKit environment variables
        os.environ.setdefault('LIVEKIT_API_KEY', 'APITMKfqYVjk79h')
        os.environ.setdefault('LIVEKIT_API_SECRET', 'gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA')
        os.environ.setdefault('LIVEKIT_URL', 'wss://sr-fa31r2za.livekit.cloud')
        os.environ.setdefault('PORT', '5000')
        
        print("✅ LiveKit environment configured")
        return True
        
    def start_web_server(self):
        """Start the Flask web server in a separate process"""
        print("🌐 Starting Web Server...")
        try:
            self.web_process = subprocess.Popen([
                sys.executable, 'web_server.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
               universal_newlines=True, bufsize=1)
            
            # Monitor web server output
            if self.web_process.stdout:
                for line in iter(self.web_process.stdout.readline, ''):
                    if self.stop_event.is_set():
                        break
                    print(f"[WEB] {line.strip()}")
                
        except Exception as e:
            print(f"❌ Failed to start web server: {e}")
            
    def start_voice_agent(self):
        """Start the voice agent in a separate process"""
        print("🤖 Starting Alex Voice Agent...")
        try:
            # Use LiveKit agents CLI for proper connection handling
            self.agent_process = subprocess.Popen([
                sys.executable, '-m', 'livekit.agents.cli', 'dev', 'agent.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
               universal_newlines=True, bufsize=1)
            
            # Monitor agent output
            if self.agent_process.stdout:
                for line in iter(self.agent_process.stdout.readline, ''):
                    if self.stop_event.is_set():
                        break
                    print(f"[AGENT] {line.strip()}")
                
        except Exception as e:
            print(f"❌ Failed to start voice agent: {e}")
            
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n🛑 Shutting down Alex Voice Agent...")
        self.stop_event.set()
        
        if self.web_process:
            self.web_process.terminate()
            
        if self.agent_process:
            self.agent_process.terminate()
            
        print("✅ Alex Voice Agent stopped")
        sys.exit(0)
        
    def run(self):
        """Main runner - starts both services"""
        print("🚀 Alex Voice Agent - GitHub Codespaces Launcher")
        print("=" * 50)
        
        # Check environment
        if not self.check_environment():
            return
            
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("\n🎯 Starting services...")
        print("   • Web interface will be available on port 5000")
        print("   • Check the 'Ports' tab in VS Code to access")
        print("   • Press Ctrl+C to stop both services")
        print("\n" + "=" * 50)
        
        # Start web server in background thread
        web_thread = threading.Thread(target=self.start_web_server, daemon=True)
        web_thread.start()
        
        # Give web server time to start
        time.sleep(2)
        
        # Start voice agent in background thread  
        agent_thread = threading.Thread(target=self.start_voice_agent, daemon=True)
        agent_thread.start()
        
        try:
            # Keep the main thread alive
            while not self.stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    launcher = AlexCodespaceLauncher()
    launcher.run()
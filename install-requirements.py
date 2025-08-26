#!/usr/bin/env python3
"""
Simple requirements installer for GitHub Codespaces
Works exactly like: pip install -r requirements.txt
"""

import subprocess
import sys

def main():
    print("📦 Installing Alex Voice Agent Requirements...")
    print("=" * 50)
    
    # Clean list of requirements (no duplicates)
    requirements = [
        'flask>=3.1.2',
        'google-genai>=1.31.0',
        'livekit-api>=1.0.5',
        'livekit>=1.0.12',
        'livekit-agents>=1.2.6',
        'livekit-plugins-deepgram>=1.2.6',
        'livekit-plugins-elevenlabs>=1.2.6',
        'livekit-plugins-openai>=1.2.6',
        'livekit-plugins-google>=1.2.6',
        'pyjwt>=2.10.1',
        'python-dotenv>=1.0.0',
        'sift-stack-py>=0.8.4',
        'gunicorn>=21.2.0'
    ]
    
    try:
        # Install all requirements at once (faster)
        print("Installing packages...")
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install'
        ] + requirements)
        
        print("\n✅ All requirements installed successfully!")
        print("\n🚀 You can now run: python run-alex-codespace.py")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Installation failed: {e}")
        print("💡 Try running individual package installations")
        return False
    
    return True

if __name__ == "__main__":
    main()
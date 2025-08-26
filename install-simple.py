#!/usr/bin/env python3
"""
Simple installer that works in any environment
"""

import subprocess
import sys
import os

def try_install():
    packages = [
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
    
    print("🔧 Installing Alex Voice Agent packages...")
    
    # Find working Python/pip
    pip_commands = [
        ['python3', '-m', 'pip'],
        ['python', '-m', 'pip'],
        ['pip3'],
        ['pip']
    ]
    
    working_pip = None
    for cmd in pip_commands:
        try:
            subprocess.check_output(cmd + ['--version'], stderr=subprocess.DEVNULL)
            working_pip = cmd
            print(f"✅ Found working pip: {' '.join(cmd)}")
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if not working_pip:
        print("❌ No working pip found. Try installing pip first.")
        return False
    
    # Install packages
    try:
        cmd = working_pip + ['install'] + packages
        print("📦 Installing all packages...")
        subprocess.check_call(cmd)
        print("✅ All packages installed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

if __name__ == "__main__":
    success = try_install()
    if success:
        print("🚀 Ready! Run: python run-alex-codespace.py")
    sys.exit(0 if success else 1)
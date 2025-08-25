#!/usr/bin/env python3
"""
GitHub Codespaces dependency installer
Run this if packages are missing: python install-codespace-deps.py
"""

import subprocess
import sys

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', package, '--user'
        ])
        return True
    except subprocess.CalledProcessError:
        return False

def check_package(package):
    """Check if a package is installed"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    print("🔧 GitHub Codespaces - Installing Alex Voice Agent Dependencies")
    print("=" * 60)
    
    # List of required packages
    packages = [
        'flask>=3.1.2',
        'google-genai>=1.31.0',
        'livekit-api>=1.0.5',
        'livekit>=1.0.12',
        'livekit-agents>=1.2.6',
        'livekit-plugins-deepgram>=1.2.6',
        'livekit-plugins-elevenlabs>=1.2.6',
        'livekit-plugins-openai>=1.2.6',
        'pyjwt>=2.10.1',
        'sift-stack-py>=0.8.4',
        'livekit-plugins-google>=1.2.6',
        'gunicorn>=21.2.0',
        'python-dotenv>=1.0.0'
    ]
    
    print("📦 Installing packages...")
    for package in packages:
        package_name = package.split('>=')[0].replace('-', '_')
        if not check_package(package_name.split('.')[-1]):  # Check base name
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✅ {package} installed")
            else:
                print(f"❌ Failed to install {package}")
        else:
            print(f"✅ {package} already installed")
    
    print("\n🔍 Verifying installations...")
    
    # Verify key imports
    test_imports = [
        ('flask', 'Flask'),
        ('livekit', 'LiveKit'),
        ('google.genai', 'Google GenAI'),
        ('livekit.agents', 'LiveKit Agents'),
    ]
    
    for module, name in test_imports:
        try:
            __import__(module)
            print(f"✅ {name} - OK")
        except ImportError as e:
            print(f"❌ {name} - {e}")
    
    print(f"\n🚀 Ready! Run your Alex Voice Agent with:")
    print(f"   python run-alex-codespace.py")

if __name__ == "__main__":
    main()
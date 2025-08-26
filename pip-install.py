#!/usr/bin/env python3
"""
Wrapper to make 'pip install -r requirements.txt' work properly
Handles duplicate entries automatically

Usage: python pip-install.py
       python pip-install.py requirements.txt
"""

import subprocess
import sys
import os

def clean_requirements(file_path="requirements.txt"):
    """Remove duplicate packages from requirements file"""
    if not os.path.exists(file_path):
        print(f"❌ {file_path} not found")
        return None
    
    seen = set()
    clean_lines = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            # Extract package name (before version specifier)
            pkg_name = line.split('>=')[0].split('==')[0].split('~=')[0].split('<')[0]
            if pkg_name not in seen:
                seen.add(pkg_name)
                clean_lines.append(line)
    
    return clean_lines

def main():
    req_file = sys.argv[1] if len(sys.argv) > 1 else "requirements.txt"
    
    print(f"📦 Processing {req_file}...")
    
    # Clean requirements
    clean_reqs = clean_requirements(req_file)
    if not clean_reqs:
        return 1
    
    print(f"📋 Found {len(clean_reqs)} unique packages")
    
    try:
        # Install packages directly
        cmd = [sys.executable, '-m', 'pip', 'install'] + clean_reqs
        print("🔧 Installing packages...")
        subprocess.check_call(cmd)
        
        print("\n✅ All packages installed successfully!")
        print("🚀 Run: python run-alex-codespace.py")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
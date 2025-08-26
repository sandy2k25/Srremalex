#!/usr/bin/env python3
"""
Fix requirements.txt and install packages properly
Makes 'pip install -r requirements.txt' work correctly
"""

import subprocess
import sys
import tempfile
import os

def fix_and_install():
    print("🔧 Fixing requirements.txt and installing packages...")
    
    # Read original requirements.txt
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()
    
    # Remove duplicates while preserving order
    seen = set()
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            # Extract package name (before version specifier)
            pkg_name = line.split('>=')[0].split('==')[0].split('~=')[0].split('<')[0].strip()
            if pkg_name not in seen:
                seen.add(pkg_name)
                clean_lines.append(line)
    
    print(f"📋 Found {len(clean_lines)} unique packages (removed duplicates)")
    
    # Create temporary clean requirements file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
        tmp_file.write('\n'.join(clean_lines))
        tmp_file_path = tmp_file.name
    
    try:
        # Install using pip with clean requirements
        print("📦 Installing packages...")
        
        # Try multiple Python/pip combinations
        install_commands = [
            ['python3', '-m', 'pip', 'install', '-r', tmp_file_path],
            ['python', '-m', 'pip', 'install', '-r', tmp_file_path],
            ['pip3', 'install', '-r', tmp_file_path],
            ['pip', 'install', '-r', tmp_file_path]
        ]
        
        success = False
        for cmd in install_commands:
            try:
                print(f"Trying: {' '.join(cmd)}")
                subprocess.check_call(cmd)
                success = True
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        if not success:
            raise subprocess.CalledProcessError(1, "All pip install attempts failed")
            
        print("✅ All packages installed successfully!")
        print("🚀 You can now run: python run-alex-codespace.py")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)
    
    return True

if __name__ == "__main__":
    success = fix_and_install()
    sys.exit(0 if success else 1)
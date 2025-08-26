#!/bin/bash
# Script to make 'pip install -r requirements.txt' work properly
# Usage: bash install-reqs.sh  OR  ./install-reqs.sh

echo "📦 Installing requirements (handling duplicates)..."

# Create temporary clean requirements file
python3 -c "
import sys
seen = set()
with open('requirements.txt', 'r') as f:
    lines = f.readlines()

clean_lines = []
for line in lines:
    line = line.strip()
    if line and not line.startswith('#'):
        pkg_name = line.split('>=')[0].split('==')[0].split('~=')[0]
        if pkg_name not in seen:
            seen.add(pkg_name)
            clean_lines.append(line)

with open('requirements-temp.txt', 'w') as f:
    f.write('\n'.join(clean_lines))
"

# Install from clean requirements
pip install -r requirements-temp.txt

# Clean up
rm requirements-temp.txt

echo "✅ Requirements installed successfully!"
echo "🚀 You can now run: python run-alex-codespace.py"
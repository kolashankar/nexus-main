#!/usr/bin/env python3
"""Fix all backend imports to use correct module paths."""

import os
import re
from pathlib import Path

# Patterns to replace
PATTERNS = [
    (r'^from core\.', 'from backend.core.'),
    (r'^from models\.', 'from backend.models.'),
    (r'^from services\.', 'from backend.services.'),
    (r'^from utils\.', 'from backend.utils.'),
    (r'^from api\.', 'from backend.api.'),
    (r'^from middleware\.', 'from backend.middleware.'),
]

def fix_file(filepath):
    """Fix imports in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        fixed_line = line
        for pattern, replacement in PATTERNS:
            if re.match(pattern, line.strip()):
                fixed_line = re.sub(pattern, replacement, line)
                break
        fixed_lines.append(fixed_line)
    
    fixed_content = '\n'.join(fixed_lines)
    
    if fixed_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True
    return False

def main():
    """Main function."""
    backend_dir = Path('/app/backend')
    fixed_count = 0
    
    # Find all Python files
    for py_file in backend_dir.rglob('*.py'):
        if py_file.name == 'fix_imports.py':
            continue
        if fix_file(py_file):
            print(f"Fixed: {py_file}")
            fixed_count += 1
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == '__main__':
    main()

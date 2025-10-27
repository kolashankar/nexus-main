#!/usr/bin/env python3
"""
TypeScript to JavaScript converter for Karma Nexus 2.0
Converts all .ts and .tsx files to .js and .jsx
"""

import os
import re
import shutil
from pathlib import Path

def remove_type_annotations(content):
    """Remove TypeScript type annotations from code"""
    
    # Remove interface declarations
    content = re.sub(r'export\s+interface\s+\w+\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    content = re.sub(r'interface\s+\w+\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    
    # Remove type aliases
    content = re.sub(r'export\s+type\s+\w+\s*=\s*[^;]+;', '', content)
    content = re.sub(r'type\s+\w+\s*=\s*[^;]+;', '', content)
    
    # Remove enum declarations - convert to objects
    content = re.sub(r'export\s+enum\s+(\w+)\s*\{', r'export const \1 = {', content)
    content = re.sub(r'enum\s+(\w+)\s*\{', r'const \1 = {', content)
    
    # Remove type parameters from functions and classes
    content = re.sub(r'<[^>]*>', '', content)
    
    # Remove type annotations from function parameters
    content = re.sub(r'(\w+):\s*[^,)=]+([,)])', r'\1\2', content)
    
    # Remove return type annotations
    content = re.sub(r'(\)):\s*[^{=>\n]+([{=>\n])', r'\1\2', content)
    
    # Remove property type annotations
    content = re.sub(r'(\w+):\s*[^;=\n]+;', r'\1;', content)
    
    # Remove as type assertions
    content = re.sub(r'\s+as\s+\w+', '', content)
    
    # Remove ! non-null assertions
    content = re.sub(r'!\.', '.', content)
    content = re.sub(r'!\[', '[', content)
    content = re.sub(r'!\)', ')', content)
    
    # Remove generic constraints
    content = re.sub(r'extends\s+\w+(\s*[,>])', r'\1', content)
    
    # Fix const assertions
    content = content.replace(' as const', '')
    
    return content

def convert_imports(content):
    """Convert TypeScript imports to JavaScript"""
    # Change .ts imports to .js
    content = re.sub(r"from\s+['\"]([^'\"]+)\.ts['\"]", r"from '\1.js'", content)
    content = re.sub(r"from\s+['\"]([^'\"]+)\.tsx['\"]", r"from '\1.jsx'", content)
    
    # Remove type-only imports
    content = re.sub(r"import\s+type\s+\{[^}]+\}\s+from\s+['\"][^'\"]+['\"];?\n", '', content)
    content = re.sub(r"import\s+\{[^}]*type\s+[^}]*\}\s+from\s+['\"][^'\"]+['\"];?\n", '', content)
    
    return content

def convert_file(ts_path, js_path):
    """Convert a single TypeScript file to JavaScript"""
    try:
        with open(ts_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert imports
        content = convert_imports(content)
        
        # Remove type annotations
        content = remove_type_annotations(content)
        
        # Write JavaScript file
        os.makedirs(os.path.dirname(js_path), exist_ok=True)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error converting {ts_path}: {e}")
        return False

def main():
    frontend_dir = Path('/app/frontend')
    src_dir = frontend_dir / 'src'
    
    converted_count = 0
    failed_count = 0
    
    # Find all .ts and .tsx files
    ts_files = list(src_dir.rglob('*.ts')) + list(src_dir.rglob('*.tsx'))
    
    # Also convert root config files
    root_ts_files = list(frontend_dir.glob('*.ts'))
    ts_files.extend(root_ts_files)
    
    print(f"Found {len(ts_files)} TypeScript files to convert")
    
    for ts_path in ts_files:
        # Skip .d.ts files
        if ts_path.suffix == '.ts' and ts_path.stem.endswith('.d'):
            print(f"Skipping definition file: {ts_path}")
            continue
        
        # Determine output path
        if ts_path.suffix == '.tsx':
            js_path = ts_path.with_suffix('.jsx')
        else:
            js_path = ts_path.with_suffix('.js')
        
        print(f"Converting: {ts_path.relative_to(frontend_dir)} -> {js_path.name}")
        
        if convert_file(ts_path, js_path):
            converted_count += 1
        else:
            failed_count += 1
    
    print(f"\nConversion complete!")
    print(f"✅ Successfully converted: {converted_count} files")
    print(f"❌ Failed: {failed_count} files")
    
    return converted_count, failed_count

if __name__ == '__main__':
    main()

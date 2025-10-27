#!/usr/bin/env python3
"""
Fix JavaScript syntax issues after TypeScript conversion
"""

import os
import re
from pathlib import Path

def fix_jsx_elements(content):
    """Fix JSX element syntax issues"""
    # Fix broken JSX tags like: } />
    content = re.sub(r'}\s+/>', r'} />', content)
    
    # Fix incomplete elements: return ;
    content = re.sub(r'return\s+;', r'return null;', content)
    
    # Fix broken JSX: return {children};
    content = re.sub(r'return\s+\{children\};', r'return <>{children}</>;', content)
    
    # Fix missing JSX content: <Element />
    # This is actually okay, just verify it's complete
    
    return content

def fix_type_imports(content):
    """Remove any remaining type imports"""
    # Remove type-only imports
    content = re.sub(r'import\s+type\s+\{[^}]+\}\s+from\s+[\'"][^\'"]+[\'"];?\s*\n', '', content)
    
    # Remove individual type imports from regular imports
    content = re.sub(r'import\s+\{([^}]*?)type\s+\w+,?\s*([^}]*?)\}\s+from', r'import {\1\2} from', content)
    
    return content

def fix_interface_exports(content):
    """Remove any remaining interface/type exports"""
    # Remove export interface
    content = re.sub(r'export\s+interface\s+\w+\s*\{[^}]*\}', '', content, flags=re.DOTALL)
    
    # Remove export type
    content = re.sub(r'export\s+type\s+\w+\s*=[^;]+;', '', content)
    
    return content

def fix_function_syntax(content):
    """Fix function parameter and return type remnants"""
    # Fix const Component: React.FC = (props) =>
    content = re.sub(r'const\s+(\w+):\s*React\.FC\w*\s*=\s*\(\s*\{([^}]*)\}\s*\)', r'const \1 = ({ \2 })', content)
    
    # Fix function Component: React.FC = 
    content = re.sub(r'function\s+(\w+):\s*React\.FC', r'function \1', content)
    
    return content

def fix_generic_remnants(content):
    """Remove any remaining generic syntax"""
    # Fix Map<string, any> -> Map
    content = re.sub(r'Map<[^>]+>', 'Map', content)
    content = re.sub(r'Set<[^>]+>', 'Set', content)
    content = re.sub(r'Array<[^>]+>', 'Array', content)
    content = re.sub(r'Promise<[^>]+>', 'Promise', content)
    
    return content

def fix_as_assertions(content):
    """Remove 'as' type assertions"""
    content = re.sub(r'\s+as\s+\w+(\[|\.|\)|\,|\;)', r'\1', content)
    content = re.sub(r'\s+as\s+any', '', content)
    
    return content

def process_file(file_path):
    """Process a single JavaScript file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all fixes
        content = fix_jsx_elements(content)
        content = fix_type_imports(content)
        content = fix_interface_exports(content)
        content = fix_function_syntax(content)
        content = fix_generic_remnants(content)
        content = fix_as_assertions(content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    frontend_dir = Path('/app/frontend/src')
    
    # Find all JS and JSX files
    js_files = list(frontend_dir.rglob('*.js')) + list(frontend_dir.rglob('*.jsx'))
    
    print(f"Processing {len(js_files)} JavaScript files...")
    
    fixed_count = 0
    for js_file in js_files:
        if process_file(js_file):
            fixed_count += 1
            print(f"Fixed: {js_file.relative_to(frontend_dir)}")
    
    print(f"\nFixed {fixed_count} files")
    return fixed_count

if __name__ == '__main__':
    main()

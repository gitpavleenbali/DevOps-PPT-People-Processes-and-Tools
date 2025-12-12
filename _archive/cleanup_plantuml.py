#!/usr/bin/env python3
"""
PlantUML Cleanup Script - Version 2

This script removes the PlantUML source code from HTML comments,
keeping only the rendered image URLs. The original PlantUML source
is preserved in _archive/plantuml-source/*.puml files.

Output format:
<!-- Diagram: diagram_name | Source: _archive/plantuml-source/diagram_name.puml -->
![Diagram Name](https://www.plantuml.com/plantuml/svg/...)
"""

import os
import re
from pathlib import Path

def clean_file(filepath: Path) -> tuple:
    """Remove PlantUML code from HTML comments, keep only image URLs."""
    content = filepath.read_text(encoding='utf-8')
    original_length = len(content)
    
    # Pattern to match the full block:
    # <!-- PlantUML Diagram: XXX ... -->
    # ![...](URL)
    # <!-- ```plantuml ... ``` -->
    
    # This pattern matches the backup comment block with plantuml code
    pattern = r'<!--\s*\n```plantuml\n.*?```\s*\n-->'
    
    # Count matches
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if not matches:
        return 0, 0
    
    # Remove all backup comment blocks
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Clean up extra blank lines (more than 2 consecutive)
    new_content = re.sub(r'\n{4,}', '\n\n\n', new_content)
    
    # Write back
    filepath.write_text(new_content, encoding='utf-8')
    
    bytes_saved = original_length - len(new_content)
    return len(matches), bytes_saved

def main():
    # Paths
    base_dir = Path(r"c:\Users\pavleenbali\OneDrive - Microsoft\Desktop\Desk Case\MS Space\CSA\Customer Siemens\Requirement Management\DevOps PPT - People_Processes_Tools")
    
    # Files to clean
    files_to_clean = [
        base_dir / "UTM - Unified Test Management" / "01-UTM-BLUEPRINT.md",
        base_dir / "UTM - Unified Test Management" / "02-TESTING-LAYERS-TOOLING.md",
        base_dir / "UTM - Unified Test Management" / "03-TEST-STRATEGY-EXECUTION.md",
        base_dir / "USCM - Unified Service Capability Management" / "USCM-Framework.md",
    ]
    
    total_removed = 0
    total_bytes = 0
    
    print("=" * 60)
    print("PlantUML Cleanup - Removing Backup Code Blocks")
    print("=" * 60)
    print("\nNote: Original PlantUML source preserved in:")
    print("      _archive/plantuml-source/*.puml")
    print()
    
    for filepath in files_to_clean:
        if not filepath.exists():
            print(f"⚠️  Skipping (not found): {filepath.name}")
            continue
        
        print(f"📄 Cleaning: {filepath.name}")
        
        count, bytes_saved = clean_file(filepath)
        
        if count > 0:
            print(f"   ✅ Removed {count} backup blocks ({bytes_saved:,} bytes saved)")
            total_removed += count
            total_bytes += bytes_saved
        else:
            print(f"   ℹ️  No backup blocks found")
    
    print("\n" + "=" * 60)
    print(f"✅ Total: {total_removed} backup blocks removed")
    print(f"💾 Space saved: {total_bytes:,} bytes ({total_bytes/1024:.1f} KB)")
    print("=" * 60)

if __name__ == "__main__":
    main()

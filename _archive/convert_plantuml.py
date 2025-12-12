#!/usr/bin/env python3
"""
PlantUML to Proxy URL Converter

This script:
1. Extracts PlantUML code blocks from markdown files
2. Archives the original PlantUML source
3. Generates PlantUML proxy URLs (works on GitHub and VS Code)
4. Replaces ```plantuml blocks with image markdown + HTML comment backup

Proxy URL format: https://www.plantuml.com/plantuml/svg/~1{deflated_base64}
"""

import os
import re
import zlib
import base64
from pathlib import Path

# PlantUML encoding - custom base64 alphabet
PLANTUML_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
BASE64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def encode_plantuml(text: str) -> str:
    """Encode PlantUML text to URL-safe format."""
    # Compress with zlib (deflate)
    compressed = zlib.compress(text.encode('utf-8'), 9)[2:-4]  # Remove zlib header/trailer
    
    # Base64 encode
    b64 = base64.b64encode(compressed).decode('ascii')
    
    # Translate to PlantUML alphabet
    result = ""
    for char in b64:
        if char == '=':
            continue  # Skip padding
        idx = BASE64_ALPHABET.index(char)
        result += PLANTUML_ALPHABET[idx]
    
    return result

def generate_proxy_url(plantuml_code: str, format: str = "svg") -> str:
    """Generate PlantUML proxy URL."""
    encoded = encode_plantuml(plantuml_code)
    return f"https://www.plantuml.com/plantuml/{format}/{encoded}"

def extract_plantuml_blocks(content: str) -> list:
    """Extract all PlantUML code blocks from markdown content."""
    pattern = r'```plantuml\s*\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)
    return matches

def create_replacement(plantuml_code: str, diagram_name: str) -> str:
    """Create replacement markdown with proxy URL and archived source in HTML comment."""
    url = generate_proxy_url(plantuml_code)
    
    # Clean diagram name for alt text
    alt_text = diagram_name.replace('_', ' ').title()
    
    replacement = f"""<!-- PlantUML Diagram: {diagram_name}
Original source archived in _archive/plantuml-source/{diagram_name}.puml
-->
![{alt_text}]({url})

<!--
```plantuml
{plantuml_code.strip()}
```
-->"""
    
    return replacement

def process_file(filepath: Path, archive_dir: Path, file_prefix: str) -> tuple:
    """Process a markdown file, extracting and converting PlantUML blocks."""
    content = filepath.read_text(encoding='utf-8')
    
    # Find all plantuml blocks with their full match
    pattern = r'```plantuml\s*\n(.*?)```'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if not matches:
        return content, 0
    
    # Process from end to start (to maintain positions)
    diagram_count = 0
    new_content = content
    
    for i, match in enumerate(reversed(matches)):
        diagram_count += 1
        idx = len(matches) - i  # 1-based index
        plantuml_code = match.group(1)
        
        # Generate diagram name
        diagram_name = f"{file_prefix}_diagram_{idx:02d}"
        
        # Save original source to archive
        archive_file = archive_dir / f"{diagram_name}.puml"
        archive_file.write_text(plantuml_code.strip(), encoding='utf-8')
        
        # Create replacement
        replacement = create_replacement(plantuml_code, diagram_name)
        
        # Replace in content
        new_content = new_content[:match.start()] + replacement + new_content[match.end():]
    
    return new_content, len(matches)

def main():
    # Paths
    base_dir = Path(r"c:\Users\pavleenbali\OneDrive - Microsoft\Desktop\Desk Case\MS Space\CSA\Customer Siemens\Requirement Management\DevOps PPT - People_Processes_Tools")
    archive_dir = base_dir / "_archive" / "plantuml-source"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Files to process
    files_to_process = [
        (base_dir / "UTM - Unified Test Management" / "01-UTM-BLUEPRINT.md", "UTM_01_Blueprint"),
        (base_dir / "UTM - Unified Test Management" / "02-TESTING-LAYERS-TOOLING.md", "UTM_02_Testing"),
        (base_dir / "UTM - Unified Test Management" / "03-TEST-STRATEGY-EXECUTION.md", "UTM_03_Strategy"),
        (base_dir / "USCM - Unified Service Capability Management" / "USCM-Framework.md", "USCM_Framework"),
        (base_dir / "URM - Unified Requirements Management" / "URM-Blueprint.md", "URM_Blueprint"),
    ]
    
    total_diagrams = 0
    
    print("=" * 60)
    print("PlantUML to Proxy URL Converter")
    print("=" * 60)
    
    for filepath, prefix in files_to_process:
        if not filepath.exists():
            print(f"⚠️  Skipping (not found): {filepath.name}")
            continue
        
        print(f"\n📄 Processing: {filepath.name}")
        
        new_content, count = process_file(filepath, archive_dir, prefix)
        
        if count > 0:
            # Write updated file
            filepath.write_text(new_content, encoding='utf-8')
            print(f"   ✅ Converted {count} PlantUML diagrams")
            total_diagrams += count
        else:
            print(f"   ℹ️  No PlantUML diagrams found")
    
    print("\n" + "=" * 60)
    print(f"✅ Total: {total_diagrams} diagrams converted")
    print(f"📁 Archives saved to: {archive_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()

"""
Convert scraped JSON data to markdown files optimized for AI Foundry knowledge upload.
AI Foundry will automatically chunk and vectorize these markdown files.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def convert_json_to_markdown():
    """Convert all JSON files in scraped_data/ to markdown files in knowledge_sources/"""
    
    scraped_data_dir = Path("scraped_data")
    output_dir = Path("knowledge_sources")
    output_dir.mkdir(exist_ok=True)
    
    json_files = list(scraped_data_dir.glob("*.json"))
    
    if not json_files:
        print(f"❌ No JSON files found in {scraped_data_dir}")
        return False
    
    print(f"📂 Found {len(json_files)} JSON files to convert\n")
    
    for json_file in json_files:
        print(f"📄 Processing: {json_file.name}")
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Extract fields
            source_url = data.get("source_url", "")
            title = data.get("title", "")
            content = data.get("content", "")
            timestamp = data.get("timestamp", "")
            metadata = data.get("metadata", {})
            
            # Create markdown content
            markdown_content = f"""# {title}

**Source:** [{source_url}]({source_url})

**Scraped:** {timestamp}

**Metadata:**
- Characters: {metadata.get('char_count', 'N/A')}
- Words: {metadata.get('word_count', 'N/A')}

---

## Content

{content}

---

*This document was automatically converted from scraped web content for use in AI Foundry knowledge bases.*
"""
            
            # Generate output filename from the JSON filename
            output_filename = json_file.stem + ".md"
            output_path = output_dir / output_filename
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            
            print(f"   ✅ Created: {output_path}")
            print(f"   📊 Size: {len(markdown_content)} characters\n")
            
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON decode error: {e}\n")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            return False
    
    print(f"✨ Conversion complete! Markdown files ready in: {output_dir.absolute()}")
    return True

if __name__ == "__main__":
    success = convert_json_to_markdown()
    exit(0 if success else 1)

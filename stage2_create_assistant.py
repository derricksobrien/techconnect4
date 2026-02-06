"""
Stage 2: Create AI Assistant with knowledge sources using AI Foundry REST API
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Optional
import sys

# Fix encoding for Windows PowerShell
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class AIFoundryAssistant:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.headers = {
            "api-key": api_key,
            "Content-Type": "application/json"
        }
    
    def upload_file(self, file_path: Path) -> Optional[str]:
        """Upload a markdown file and return file ID"""
        try:
            # Try different endpoint variations
            urls_to_try = [
                f"{self.endpoint}/files",
                f"{self.endpoint}/files/upload",
                f"{self.endpoint.replace('/projects/', '/hubs/')}/files"
            ]
            
            with open(file_path, "rb") as f:
                file_content = f.read()
            
            for url in urls_to_try:
                try:
                    with open(file_path, "rb") as f:
                        files = {"file": (file_path.name, f)}
                        response = requests.post(url, files=files, headers={"api-key": self.api_key}, timeout=10)
                    
                    if response.status_code == 200 or response.status_code == 201:
                        data = response.json()
                        file_id = data.get("id") or data.get("file_id")
                        print(f"   ✅ Uploaded {file_path.name} → ID: {file_id}")
                        return file_id
                except:
                    continue
            
            print(f"   ❌ All upload endpoints failed for {file_path.name}")
            return None
            
        except Exception as e:
            print(f"   ❌ Upload error: {e}")
            return None
    
    def create_assistant(self, name: str, instructions: str, file_ids: List[str]) -> Optional[str]:
        """Create an assistant with file search enabled"""
        try:
            url = f"{self.endpoint}/assistants"
            
            payload = {
                "name": name,
                "instructions": instructions,
                "model": "gpt-4o",
                "tools": [{"type": "file_search"}],
                "tool_resources": {
                    "file_search": {
                        "vector_store_ids": []
                    }
                }
            }
            
            # Add file IDs if provided
            if file_ids:
                payload["tool_resources"]["file_search"]["vector_store_ids"] = file_ids
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            assistant_id = data.get("id") or data.get("assistant_id")
            print(f"✅ Assistant created → ID: {assistant_id}")
            return assistant_id
            
        except Exception as e:
            print(f"❌ Assistant creation failed: {e}")
            print(f"   Response: {response.text if 'response' in locals() else 'No response'}")
            return None

def main():
    # Configuration - Load from environment variables
    import os
    ENDPOINT = os.getenv("AZURE_FOUNDRY_ENDPOINT", "https://admin-1994-resource.services.ai.azure.com/api/projects/admin-1994")
    API_KEY = os.getenv("AZURE_FOUNDRY_KEY")
    if not API_KEY:
        raise ValueError("AZURE_FOUNDRY_KEY environment variable not set")
    KNOWLEDGE_DIR = Path("knowledge_sources")
    
    print("=" * 70)
    print("STAGE 2: Create AI Assistant with Knowledge Sources")
    print("=" * 70 + "\n")
    
    # Check knowledge directory
    if not KNOWLEDGE_DIR.exists():
        print(f"❌ {KNOWLEDGE_DIR} directory not found")
        return False
    
    md_files = list(KNOWLEDGE_DIR.glob("*.md"))
    if not md_files:
        print(f"❌ No markdown files found in {KNOWLEDGE_DIR}")
        return False
    
    print(f"📂 Found {len(md_files)} knowledge sources:")
    for f in md_files:
        print(f"   - {f.name} ({f.stat().st_size:,} bytes)")
    print()
    
    # Initialize client
    client = AIFoundryAssistant(ENDPOINT, API_KEY)
    
    # Upload files
    print("📤 Uploading knowledge sources...")
    file_ids = []
    for md_file in md_files:
        file_id = client.upload_file(md_file)
        if file_id:
            file_ids.append(file_id)
    
    if not file_ids:
        print("\n❌ No files uploaded successfully")
        return False
    
    print(f"\n✅ Uploaded {len(file_ids)} files\n")
    
    # Create assistant
    print("🤖 Creating AI Assistant...")
    instructions = """You are an expert assistant for Microsoft Solution Accelerators and enterprise cloud solutions.

Help users:
- Find relevant solution accelerators
- Understand implementation patterns
- Answer questions about enterprise cloud solutions
- Discover GitHub resources and best practices

Always cite sources when providing information from the knowledge base."""
    
    assistant_id = client.create_assistant(
        name="SolutionAccelerators-Assistant",
        instructions=instructions,
        file_ids=file_ids
    )
    
    if not assistant_id:
        return False
    
    # Save configuration
    config = {
        "assistant_id": assistant_id,
        "endpoint": ENDPOINT,
        "file_count": len(file_ids),
        "files": [f.name for f in md_files]
    }
    
    with open("assistant_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to assistant_config.json")
    print("\n" + "=" * 70)
    print("STAGE 2 COMPLETE ✅")
    print("=" * 70)
    print(f"Assistant ID: {assistant_id}")
    print(f"Files uploaded: {len(file_ids)}")
    print("\nNext: Run stage3_test_assistant.py to test the assistant")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

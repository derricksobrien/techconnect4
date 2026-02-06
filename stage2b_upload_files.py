"""
Upload knowledge files to AI Foundry agent
"""
import json
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

def upload_knowledge_files(agent_id: str):
    """Upload markdown files and attach to agent"""
    
    endpoint = "https://admin-1994-resource.services.ai.azure.com/api/projects/admin-1994"
    knowledge_dir = Path("knowledge_sources")
    
    print("=" * 70)
    print("STAGE 2B: Upload Knowledge Sources to Agent")
    print("=" * 70 + "\n")
    
    # Connect
    print("Connecting to AI Foundry...")
    try:
        credential = DefaultAzureCredential()
        client = AIProjectClient(endpoint=endpoint, credential=credential)
        print("SUCCESS\n")
    except Exception as e:
        print(f"FAILED: {e}")
        return False
    
    # Get files
    md_files = list(knowledge_dir.glob("*.md"))
    if not md_files:
        print("No markdown files found")
        return False
    
    print(f"Found {len(md_files)} knowledge sources\n")
    
    # Upload files - try different approaches
    print("Uploading files...")
    file_ids = []
    
    for md_file in md_files:
        print(f"  {md_file.name}...", end=" ")
        try:
            # Read file content
            with open(md_file, "rb") as f:
                # Try uploading as binary
                try:
                    response = client.agents.files.upload(
                        file_name=md_file.name,
                        file=f
                    )
                    file_id = response.id
                    file_ids.append(file_id)
                    print(f"OK (ID: {file_id})")
                except TypeError:
                    # If that doesn't work, try with Content-Type
                    f.seek(0)
                    response = client.agents.files.upload(
                        file_name=md_file.name,
                        file=f,
                        content_type="text/markdown"
                    )
                    file_id = response.id
                    file_ids.append(file_id)
                    print(f"OK (ID: {file_id})")
                    
        except Exception as e:
            print(f"FAILED - {type(e).__name__}: {str(e)[:50]}")
    
    if not file_ids:
        print("\nNo files uploaded successfully")
        return False
    
    print(f"\nUploaded {len(file_ids)} files")
    print(f"Agent ID: {agent_id}\n")
    
    # Save updated config
    config = {
        "agent_id": agent_id,
        "endpoint": endpoint,
        "files_uploaded": len(file_ids),
        "file_ids": file_ids,
        "model": "gpt-4o"
    }
    
    with open("assistant_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("Configuration updated")
    return True

if __name__ == "__main__":
    # Use the agent ID from previous stage
    agent_id = "asst_rFwMHjHtgDeQ1TprE6IEFzOh"
    success = upload_knowledge_files(agent_id)
    exit(0 if success else 1)

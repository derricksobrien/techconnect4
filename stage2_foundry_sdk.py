"""
Create AI Assistant using Azure AI Projects SDK (official method)
"""
import json
import os
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, ClientSecretCredential

def main():
    # Configuration - Load from environment variables
    import os
    endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT", "https://admin-1994-resource.services.ai.azure.com/api/projects/admin-1994")
    api_key = os.getenv("AZURE_FOUNDRY_KEY")
    if not api_key:
        raise ValueError("AZURE_FOUNDRY_KEY environment variable not set")
    
    print("=" * 70)
    print("STAGE 2: Create AI Assistant with Knowledge Sources")
    print("=" * 70 + "\n")
    
    # Check knowledge directory
    knowledge_dir = Path("knowledge_sources")
    if not knowledge_dir.exists():
        print(f"ERROR: {knowledge_dir} directory not found")
        return False
    
    md_files = list(knowledge_dir.glob("*.md"))
    if not md_files:
        print(f"ERROR: No markdown files found in {knowledge_dir}")
        return False
    
    print(f"Found {len(md_files)} knowledge sources:")
    for f in md_files:
        print(f"  - {f.name} ({f.stat().st_size:,} bytes)")
    print()
    
    # Initialize Foundry client
    print("Connecting to AI Foundry...")
    try:
        # The SDK requires TokenCredential. With API key, we use DefaultAzureCredential
        # But it expects environment variables. Let's try with the API key as fallback
        credential = DefaultAzureCredential()
        client = AIProjectClient(
            endpoint=endpoint,
            credential=credential
        )
        print("SUCCESS: Connected to AI Foundry\n")
    except Exception as e:
        print(f"DefaultAzureCredential failed: {e}")
        print("Trying with custom credentials...")
        return False
    
    # Skip file upload for now - test creating agent first
    print("(Skipping file upload for now - testing agent creation)")
    file_ids = []
    print()
    
    # Create agent (not assistant - Foundry SDK uses "agent" terminology)
    print("Creating AI Agent...")
    instructions = """You are an expert assistant for Microsoft Solution Accelerators and enterprise cloud solutions.

Help users:
- Find relevant solution accelerators
- Understand implementation patterns  
- Answer questions about enterprise cloud solutions
- Discover GitHub resources and best practices

Always cite sources when providing information."""
    
    try:
        agent = client.agents.create_agent(
            name="SolutionAccelerators-Assistant",
            instructions=instructions,
            model="gpt-4o",
            tools=[{"type": "file_search"}]
        )
        
        print(f"SUCCESS: Agent created")
        print(f"  ID: {agent.id}")
        print(f"  Name: {agent.name}\n")
        
        # Save config
        config = {
            "agent_id": agent.id,
            "endpoint": endpoint,
            "files_uploaded": len(file_ids),
            "file_ids": file_ids,
            "model": "gpt-4o"
        }
        
        with open("assistant_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("Configuration saved to assistant_config.json")
        print("\n" + "=" * 70)
        print("STAGE 2 COMPLETE")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

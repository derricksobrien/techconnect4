"""
Upload files using REST API with token-based authentication
"""
import json
import requests
from pathlib import Path
from azure.identity import DefaultAzureCredential

def get_token():
    """Get auth token using DefaultAzureCredential"""
    credential = DefaultAzureCredential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")
    return token.token

def upload_files_rest():
    """Upload knowledge files using REST API"""
    
    endpoint = "https://admin-1994-resource.services.ai.azure.com/api/projects/admin-1994"
    knowledge_dir = Path("knowledge_sources")
    agent_id = "asst_rFwMHjHtgDeQ1TprE6IEFzOh"
    
    print("=" * 70)
    print("STAGE 2B: Upload Files via REST API")
    print("=" * 70 + "\n")
    
    # Get token
    print("Getting auth token...")
    try:
        token = get_token()
        print(f"SUCCESS\n")
    except Exception as e:
        print(f"FAILED: {e}")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get files
    md_files = list(knowledge_dir.glob("*.md"))
    print(f"Found {len(md_files)} files\n")
    
    file_ids = []
    print("Uploading files...\n")
    
    for md_file in md_files:
        print(f"Uploading: {md_file.name}")
        
        # Try different upload endpoints
        endpoints_to_try = [
            f"{endpoint}/files",
            f"{endpoint}/agents/{agent_id}/files",
            f"{endpoint}/file_search/vector_store_files"
        ]
        
        success = False
        with open(md_file, "rb") as f:
            file_content = f.read()
        
        for upload_url in endpoints_to_try:
            try:
                print(f"  Trying: {upload_url.split('/api/')[-1]}", end=" ... ")
                
                # Try multipart form
                with open(md_file, "rb") as f:
                    files = {"file": (md_file.name, f, "text/markdown")}
                    response = requests.post(upload_url, files=files, headers=headers, timeout=30)
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    file_id = data.get("id") or data.get("file_id")
                    print(f"OK\n    ID: {file_id}")
                    file_ids.append(file_id)
                    success = True
                    break
                else:
                    print(f"Status {response.status_code}")
                    
            except Exception as e:
                print(f"Error: {type(e).__name__}")
        
        if not success:
            print(f"  FAILED: All endpoints returned errors\n")
    
    if file_ids:
        print(f"\nSUCCESS: Uploaded {len(file_ids)} files\n")
        
        # Save config
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
    else:
        print("FAILED: No files uploaded")
        return False

if __name__ == "__main__":
    success = upload_files_rest()
    exit(0 if success else 1)

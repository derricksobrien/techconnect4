import os
import sys
import json
from pathlib import Path
from azure.storage.blob import BlobServiceClient, ContentSettings

# --- CONFIGURATION ---
# Get connection string from environment or use provided string
# You can set this via: $env:AZURE_STORAGE_CONNECTION_STRING = "your-connection-string"
CONNECTION_STRING = os.getenv(
    "AZURE_STORAGE_CONNECTION_STRING",
    "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=techconnect123;AccountKey=MppDWgusnSESgnGg5wCbH8K7Qi5soUWqND2YxhvP/sCiEVFN1mYwxCz0qtO3yOpj137bOjMdcczI+AStbR49gA==;BlobEndpoint=https://techconnect123.blob.core.windows.net/;FileEndpoint=https://techconnect123.file.core.windows.net/;QueueEndpoint=https://techconnect123.queue.core.windows.net/;TableEndpoint=https://techconnect123.table.core.windows.net/"
)

# The name of the container (will be created if it doesn't exist)
CONTAINER_NAME = "web-scrapes"

# The directory where the scraper saved the files
LOCAL_DIRECTORY = "scraped_data"

def validate_configuration():
    """Validate that configuration is set up correctly."""
    
    # Check connection string
    if not CONNECTION_STRING or "DefaultEndpoints" not in CONNECTION_STRING:
        print("[!] ERROR: Connection string not configured")
        print("Set AZURE_STORAGE_CONNECTION_STRING environment variable")
        return False
    
    # Check local directory exists
    if not Path(LOCAL_DIRECTORY).exists():
        print(f"[!] ERROR: Local directory not found: {LOCAL_DIRECTORY}")
        return False
    
    # Check JSON files exist
    json_files = list(Path(LOCAL_DIRECTORY).glob("*.json"))
    if not json_files:
        print(f"[!] WARNING: No JSON files found in {LOCAL_DIRECTORY}")
        print("    Run scraper.py first: python scraper.py")
        return False
    
    print(f"[✓] Configuration valid")
    print(f"[✓] Container: {CONTAINER_NAME}")
    print(f"[✓] Found {len(json_files)} JSON files to upload")
    return True

def upload_json_to_azure():
    """Upload JSON files from local directory to Azure Blob Storage."""
    
    print("=" * 70)
    print("Azure Blob Storage Uploader")
    print("=" * 70)
    print()
    
    # Validate configuration
    if not validate_configuration():
        return False
    
    try:
        print("[*] Authenticating with Azure...")
        
        # Create BlobServiceClient using connection string
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        
        print(f"[+] Connected to storage account")
        
        # Get a client for the container (creates it if it doesn't exist)
        print(f"[*] Getting or creating container: {CONTAINER_NAME}")
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        if not container_client.exists():
            print(f"[*] Container doesn't exist, creating: {CONTAINER_NAME}")
            container_client.create_container()
            print(f"[+] Container created: {CONTAINER_NAME}")
        else:
            print(f"[+] Container exists: {CONTAINER_NAME}")

        # Get all JSON files to upload
        json_files = sorted(Path(LOCAL_DIRECTORY).glob("*.json"))
        
        if not json_files:
            print("[!] No JSON files found to upload")
            return False
        
        print()
        print(f"[*] Starting upload from: {LOCAL_DIRECTORY}")
        print(f"[*] Uploading {len(json_files)} files...")
        print()
        
        # Track results
        uploaded = 0
        failed = 0
        # Iterate through the local directory
        for json_file in json_files:
            filename = json_file.name
            local_file_path = str(json_file)
            file_size = json_file.stat().st_size
            
            try:
                # Create a blob client using the local file name
                blob_client = blob_service_client.get_blob_client(
                    container=CONTAINER_NAME, 
                    blob=filename
                )

                print(f"[>] Uploading: {filename} ({file_size} bytes)...", end=" ")
                
                with open(local_file_path, "rb") as data:
                    blob_client.upload_blob(
                        data, 
                        overwrite=True,
                        content_settings=ContentSettings(content_type='application/json')
                    )
                
                print("✓")
                uploaded += 1
            
            except Exception as e:
                print(f"✗ FAILED: {str(e)}")
                failed += 1
        
        print()
        print("=" * 70)
        print(f"Upload Summary")
        print("=" * 70)
        print(f"[+] Successfully uploaded: {uploaded} files")
        if failed > 0:
            print(f"[!] Failed uploads: {failed} files")
        print(f"[+] Storage account: techconnect123")
        print(f"[+] Container: {CONTAINER_NAME}")
        print(f"[+] Total size: {sum(f.stat().st_size for f in json_files)} bytes")
        print()
        
        if failed == 0:
            print("[✓] All files uploaded successfully to Azure!")
            print()
            print("Next steps:")
            print(f"  1. View in Azure Portal: Storage Accounts → techconnect123 → Containers → {CONTAINER_NAME}")
            print(f"  2. Access via Azure CLI: az storage blob list -c {CONTAINER_NAME} -a techconnect123")
            print("  3. Use data in Azure Search or other services")
            return True
        else:
            print(f"[!] {failed} file(s) failed to upload")
            return False

    except Exception as e:
        print()
        print("=" * 70)
        print("[!] FATAL ERROR")
        print("=" * 70)
        print(f"Error: {str(e)}")
        print()
        print("Troubleshooting:")
        print("  1. Check Azure login: az account show")
        print("  2. Verify storage account exists: az storage account list")
        print("  3. Check connection string is correct")
        print("  4. Ensure you have Contributor role on the storage account")
        return False

if __name__ == "__main__":
    print()
    success = upload_json_to_azure()
    print()
    
    if not success:
        sys.exit(1)
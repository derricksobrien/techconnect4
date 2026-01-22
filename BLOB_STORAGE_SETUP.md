# 📦 Azure Blob Storage Deployment Guide

## Overview

This guide explains how to deploy your scraped data to Azure Blob Storage using `blob_uploader.py`.

## Architecture

```
scraped_data/ (JSON files)
     ↓
blob_uploader.py
     ↓
Azure Storage Account
     ↓
Blob Container: "web-scrapes"
```

## Step 1: Create Azure Storage Account

### Via Azure Portal (GUI)
1. Go to [Azure Portal](https://portal.azure.com)
2. Click **+ Create a resource**
3. Search for **Storage account**
4. Click **Create**
5. Fill in:
   - **Subscription**: Your subscription
   - **Resource Group**: `rg-techconnect` (same as AI Search)
   - **Storage account name**: `techconnectstorage` (must be globally unique, lowercase alphanumeric)
   - **Region**: East US (same as other resources)
   - **Performance**: Standard
   - **Redundancy**: Locally-redundant storage (LRS)
6. Click **Review + Create** → **Create**

### Via Azure CLI
```powershell
# Create storage account
az storage account create `
  --name techconnectstorage `
  --resource-group rg-techconnect `
  --location eastus `
  --sku Standard_LRS

# Verify creation
az storage account show --name techconnectstorage --resource-group rg-techconnect
```

## Step 2: Get Connection String

### Via Azure Portal
1. Go to your Storage Account
2. Click **Access keys** in the left menu
3. Under **Key1**, copy the **Connection string**
4. It looks like: `DefaultEndpointsProtocol=https;AccountName=techconnectstorage;AccountKey=...;EndpointSuffix=core.windows.net`

### Via Azure CLI
```powershell
az storage account show-connection-string `
  --name techconnectstorage `
  --resource-group rg-techconnect `
  --query connectionString `
  -o tsv
```

## Step 3: Update Connection String in Code

Edit `blob_uploader.py` and replace line 5:

```python
# Before:
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"

# After (paste your actual connection string):
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=techconnectstorage;AccountKey=YOUR_KEY_HERE;EndpointSuffix=core.windows.net"
```

**⚠️ Security Note**: Never commit connection strings to git!

### Better: Use Environment Variables

Instead of hardcoding, use environment variable:

```python
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
```

Then set the environment variable:
```powershell
$env:AZURE_STORAGE_CONNECTION_STRING = "your-connection-string-here"
```

## Step 4: Upload to Azure

### Activate virtual environment
```powershell
cd c:\Users\derri\Code\TechConnect3
.\venv\Scripts\Activate.ps1
```

### Run the uploader
```powershell
python blob_uploader.py
```

### Expected Output
```
[*] Starting upload from: scraped_data
[>] Uploading accelerators_ms_.json...
[+] Successfully uploaded: accelerators_ms_.json
[>] Uploading aka_ms_csaGoldStandards.json...
[+] Successfully uploaded: aka_ms_csaGoldStandards.json
[>] Uploading github_com_microsoft_Solution_Accelerators.json...
[+] Successfully uploaded: github_com_microsoft_Solution_Accelerators.json
[>] Uploading github_com_microsoft_Commercial_Solution_Areas_Accelerators.json...
[+] Successfully uploaded: github_com_microsoft_Commercial_Solution_Areas_Accelerators.json
--- All files uploaded successfully to Azure! ---
```

## Step 5: Verify in Azure Portal

1. Go to your Storage Account
2. Click **Containers** in the left menu
3. You should see **web-scrapes** container
4. Click on it to see your uploaded JSON files
5. Click a file to view/download it

## How It Works

### What `blob_uploader.py` Does

```python
1. Reads CONNECTION_STRING
2. Creates BlobServiceClient
3. Gets or creates container "web-scrapes"
4. Finds all .json files in scraped_data/
5. Uploads each file with:
   - Correct content type (application/json)
   - Overwrite enabled (replaces existing)
6. Prints status for each upload
```

### Configuration Options

Edit these variables in `blob_uploader.py`:

```python
CONNECTION_STRING = "..."           # Your connection string
CONTAINER_NAME = "web-scrapes"      # Container name (auto-creates if needed)
LOCAL_DIRECTORY = "scraped_data"    # Directory with JSON files
```

## Use Cases

### 1. Archive Scraped Data
Upload raw scrapes for historical records and backup

```powershell
python blob_uploader.py
# All data backed up to Azure
```

### 2. Share with Team
Make container public or grant access to team members

```powershell
# Make container public (read-only)
az storage container set-permission `
  --name web-scrapes `
  --account-name techconnectstorage `
  --public-access blob
```

### 3. Data Pipeline
Use blob storage as input for Azure Functions/Logic Apps

```
Blob Storage → Azure Function → Process → Azure Search
```

### 4. Compliance & Backup
Keep copies in Azure for regulatory compliance

## Advanced: Setup with Environment Variables

### For Development
```powershell
# Set temporarily in current session
$env:AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=..."

# Run uploader
python blob_uploader.py
```

### For Production
Create `.env` file (add to .gitignore):
```
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
```

Update `blob_uploader.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
```

Install python-dotenv:
```powershell
pip install python-dotenv
```

## Troubleshooting

### Error: "Invalid connection string"
- ✓ Copy full connection string from Portal
- ✓ No spaces or line breaks
- ✓ Includes AccountKey=...

### Error: "Connection refused"
- ✓ Check internet connection
- ✓ Verify storage account name is correct
- ✓ Ensure region is accessible

### Error: "Invalid container name"
Container names must:
- ✓ Be lowercase
- ✓ Start with letter or number
- ✓ Contain only letters, numbers, hyphens
- ✓ Be 3-63 characters

### Files not uploading
- ✓ Check files exist in `scraped_data/`
- ✓ Verify connection string is correct
- ✓ Check storage account has space

### Connection string missing
```powershell
# Get it again
az storage account show-connection-string --name techconnectstorage --resource-group rg-techconnect --query connectionString -o tsv
```

## Integration with Other Services

### With Azure Search (Index from Blob)
```powershell
# Create indexer that pulls from blob storage
# Portal → Search Service → Data Sources → Azure Blob Storage
```

### With Azure Functions (Trigger on Upload)
```python
# Function triggers when files uploaded to blob
# Can process, transform, or index data automatically
```

### With Power BI (Analyze Data)
```powershell
# Connect Power BI to blob storage
# Visualize scraped data
```

## Cost Estimation

For 12 KB of data:
- **Storage**: ~$0.018/month (0.01 GB)
- **Operations**: <$0.001/month
- **Bandwidth**: Free (within region)

**Total**: ~$0.02/month for small data

Costs scale with data size. See [pricing](https://azure.microsoft.com/pricing/details/storage/blobs/).

## Security Best Practices

### 1. Protect Connection String
```powershell
# ❌ Don't do this
git add blob_uploader.py  # Will expose connection string

# ✅ Do this
git add blob_uploader.py
git add .gitignore  # Add CONNECTION_STRING to gitignore
```

### 2. Use Managed Identity (Production)
```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(
    account_url="https://techconnectstorage.blob.core.windows.net",
    credential=credential
)
```

### 3. Set Container Permissions
```powershell
# Private (default, best for security)
az storage container set-permission --name web-scrapes --account-name techconnectstorage --public-access off

# Blob (read-only, share with public)
az storage container set-permission --name web-scrapes --account-name techconnectstorage --public-access blob
```

### 4. Enable Soft Delete
```powershell
az storage account blob-service-properties update `
  --account-name techconnectstorage `
  --resource-group rg-techconnect `
  --enable-delete-retention true `
  --delete-retention-days 7
```

## Complete Workflow Example

```powershell
# 1. Activate environment
.\venv\Scripts\Activate.ps1

# 2. Scrape data
python scraper.py

# 3. Upload to Azure
$env:AZURE_STORAGE_CONNECTION_STRING = "your-string"
python blob_uploader.py

# 4. Verify in Azure
az storage blob list `
  --container-name web-scrapes `
  --account-name techconnectstorage `
  --query "[].name"

# 5. Download if needed
az storage blob download `
  --container-name web-scrapes `
  --name accelerators_ms_.json `
  --account-name techconnectstorage `
  --file downloaded.json
```

## Next Steps

1. **Create storage account** (Portal or CLI)
2. **Copy connection string**
3. **Update blob_uploader.py** with connection string
4. **Run uploader**: `python blob_uploader.py`
5. **Verify** in Azure Portal

## Resources

- [Azure Blob Storage Docs](https://learn.microsoft.com/azure/storage/blobs/)
- [Python SDK](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/storage/azure-storage-blob)
- [Blob Naming Rules](https://learn.microsoft.com/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata)
- [Security Best Practices](https://learn.microsoft.com/azure/storage/common/security-baseline-azure-storage)

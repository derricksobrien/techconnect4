# 🚀 Quick Blob Storage Upload

## What You Need

1. **Azure Storage Account** - Created in Azure
2. **Connection String** - From Azure Portal
3. **blob_uploader.py** - Already in your project ✅
4. **azure-storage-blob** - Already installed ✅

## 3-Step Setup

### Step 1: Create Storage Account (Azure Portal)

1. Go to https://portal.azure.com
2. Click **+ Create resource**
3. Search for **Storage account** → **Create**
4. Fill in:
   - Name: `techconnectstorage` (must be unique)
   - Region: East US (same as other resources)
   - Click **Review + Create** → **Create**

⏳ Wait ~2 minutes for deployment

### Step 2: Get Connection String

1. Go to your Storage Account
2. Click **Access keys** (left menu)
3. Copy the **Connection string** under Key1
4. Paste somewhere safe (you'll need it in 30 seconds)

### Step 3: Run Uploader

```powershell
# Activate environment
cd c:\Users\derri\Code\TechConnect3
.\venv\Scripts\Activate.ps1

# Set connection string (paste your actual string)
$env:AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=techconnectstorage;AccountKey=YOUR_KEY_HERE..."

# Run uploader
python blob_uploader.py
```

## Expected Output

```
======================================================================
Azure Blob Storage Uploader
======================================================================

[✓] Configuration valid
[✓] Found 4 JSON files to upload
[*] Connecting to Azure Storage...
[*] Getting or creating container: web-scrapes
[+] Container exists: web-scrapes

[*] Starting upload from: scraped_data
[*] Uploading 4 files...

[>] Uploading: accelerators_ms_.json (9870 bytes)... ✓
[>] Uploading: aka_ms_csaGoldStandards.json (420 bytes)... ✓
[>] Uploading: github_com_microsoft_Solution_Accelerators.json (1790 bytes)... ✓
[>] Uploading: github_com_microsoft_Commercial_Solution_Areas_Accelerators.json (400 bytes)... ✓

======================================================================
Upload Summary
======================================================================
[+] Successfully uploaded: 4 files
[+] Container: web-scrapes
[+] Total size: 12480 bytes

[✓] All files uploaded successfully to Azure!

Next steps:
  1. View in Azure Portal: Storage Accounts → Containers → web-scrapes
  2. Use data in Azure Search or other services
  3. Download if needed: az storage blob download ...
```

## Verify Upload

### In Azure Portal
1. Go to your Storage Account
2. Click **Containers**
3. Click **web-scrapes**
4. You should see 4 JSON files

### Via Command Line
```powershell
# List uploaded files
az storage blob list `
  --container-name web-scrapes `
  --account-name techconnectstorage `
  --query "[].name"
```

## That's It! ✅

Your data is now in Azure Blob Storage and ready to:
- Use with Azure Search
- Process with Azure Functions
- Share with your team
- Back up your scraped data

## Troubleshooting

**Q: "Invalid connection string"**
```powershell
# Copy again from Azure Portal → Access keys
# Paste the ENTIRE connection string
```

**Q: "Container not found"**
- Script auto-creates it, but verify storage account exists

**Q: "No JSON files"**
```powershell
# Run scraper first
python scraper.py
```

**Q: "Connection refused"**
- Check internet
- Verify storage account name is correct

## For More Details

See [BLOB_STORAGE_SETUP.md](BLOB_STORAGE_SETUP.md) for complete guide with:
- CLI setup
- Environment variables
- Security best practices
- Integration examples
- Troubleshooting

---

**Done!** Your data is now on Azure. 🎉

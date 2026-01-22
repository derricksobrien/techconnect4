# TechConnect3: Azure AI Search with LLM Grounding

This project scrapes GitHub repositories and Microsoft documentation to build a searchable knowledge base for grounding LLM models in Azure AI Search.

## Architecture

```
scraper.py → scraped_data/ (JSON) → azure_search_indexer.py → Azure AI Search → LLM Grounding
```

## Prerequisites

- Python 3.10+
- Azure Subscription with:
  - Azure AI Search service (formerly Cognitive Search)
  - Azure OpenAI (or similar LLM) - optional for grounding
- Windows/Linux/macOS

## Setup

### 1. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install playwright beautifulsoup4 azure-search-documents azure-identity
python -m playwright install chromium
```

### 3. Configure Azure Credentials

The project uses Azure DefaultAzureCredential, which supports multiple authentication methods:

**Option A: Azure CLI (Easiest)**
```powershell
az login
```

**Option B: Environment Variables**
```powershell
$env:AZURE_SUBSCRIPTION_ID = "your-subscription-id"
$env:AZURE_TENANT_ID = "your-tenant-id"
$env:AZURE_CLIENT_ID = "your-client-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
```

**Option C: Visual Studio/IDE Integration**
Just use your IDE's built-in Azure login.

### 4. Set Azure Search Endpoint

```powershell
$env:AZURE_SEARCH_ENDPOINT = "https://your-service-name.search.windows.net"
```

## Usage

### Step 1: Scrape Data

```powershell
.\venv\Scripts\python.exe scraper.py
```

This will:
- Crawl the target URLs (Microsoft Accelerators, GitHub repos, etc.)
- Extract content using Playwright (handles JavaScript-rendered pages)
- Save JSON files in `scraped_data/` directory
- Each file contains: URL, title, content, and metadata

**Output Structure:**
```
scraped_data/
├── accelerators_ms_.json
├── aka_ms_csaGoldStandards.json
├── github_com_microsoft_Solution_Accelerators.json
└── github_com_microsoft_Commercial_Solution_Areas_Accelerators.json
```

### Step 2: Create Azure AI Search Index & Index Documents

```powershell
.\venv\Scripts\python.exe azure_search_indexer.py
```

This will:
1. Create a search index with fields for your content
2. Upload all scraped documents to Azure AI Search
3. Test a sample search query
4. Print results with titles and URLs

### Step 3: Query via LLM (Example)

Once indexed, you can ground an LLM using the search results:

```python
from azure_search_indexer import AzureAISearchManager

manager = AzureAISearchManager("https://your-service.search.windows.net")

# Search for relevant context
results = manager.search("How to build solution accelerators?", top=5)

# Use these results to ground your LLM prompt
context = "\n".join([f"- {r['title']}: {r['content'][:200]}" for r in results])

llm_prompt = f"""
Based on this context:
{context}

Answer: What are Microsoft Solution Accelerators?
"""
```

## Configuration

### Target URLs (scraper.py)

Edit the `TARGET_URLS` list in `scraper.py` to scrape different repositories:

```python
TARGET_URLS = [
    "https://github.com/your-org/your-repo",
    "https://docs.microsoft.com/your-page",
    # Add more URLs...
]
```

### Search Index Fields (azure_search_indexer.py)

Modify the `create_index()` method to add custom fields:

```python
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="category", type=SearchFieldDataType.String),
    # Add more fields...
]
```

## Azure AI Search Setup

If you don't have an Azure AI Search service yet:

```powershell
# Create resource group
az group create --name rg-techconnect --location eastus

# Create Azure AI Search service
az search service create \
  --name techconnect-search \
  --resource-group rg-techconnect \
  --sku standard
```

Then set the endpoint:
```powershell
$env:AZURE_SEARCH_ENDPOINT = "https://techconnect-search.search.windows.net"
```

## Troubleshooting

### "Module not found" errors
```powershell
# Reinstall packages
pip install --upgrade -r requirements.txt
```

### Azure Authentication issues
```powershell
# Check current authentication
az account show

# Re-authenticate
az login --tenant your-tenant-id
```

### Scraper not downloading data
- Check internet connection
- Verify URLs are accessible
- Increase timeout in `scraper.py` (wait_until="networkidle")

### Search index already exists
```powershell
# Delete old index before re-running
# (You can add a --delete-existing flag to azure_search_indexer.py)
```

## Next Steps

1. **Add LLM Grounding**: Integrate with Azure OpenAI to ground responses in your indexed content
2. **Add Metadata**: Extract tags, authors, dates from source repositories
3. **Semantic Search**: Use Azure AI Search's semantic ranking for better results
4. **Custom Analyzers**: Add language-specific analyzers for better text indexing
5. **Hybrid Search**: Combine keyword search with vector embeddings for semantic search

## API Reference

### AzureAISearchManager

**`__init__(service_endpoint, index_name="techconnect-index")`**
- Initialize connection to Azure AI Search

**`create_index()`**
- Create search index with predefined schema

**`index_documents(data_dir="scraped_data")`**
- Upload JSON documents from directory to index

**`search(query, top=5)`**
- Search the index and return results

## Project Structure

```
TechConnect3/
├── scraper.py                    # Web scraper using Playwright
├── azure_search_indexer.py       # Azure AI Search integration
├── scraped_data/                 # Output folder (generated)
│   ├── *.json                    # Scraped content
├── venv/                         # Virtual environment
└── README.md                     # This file
```

## License

MIT

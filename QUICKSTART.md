# TechConnect3 Quick Start Guide

## 📋 Overview

TechConnect3 is a complete system for:
1. **Scraping** GitHub repositories and web content
2. **Indexing** data into Azure AI Search
3. **Grounding LLM responses** with real, searchable data

```
Web Content → Scraper (Playwright) → JSON Files → Azure AI Search → LLM Responses
```

## ⚡ 5-Minute Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment (venv)
- Azure subscription (for Azure AI Search)

### Step 1: Clone/Download & Setup
```powershell
cd c:\Users\derri\Code\TechConnect3

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
python -m playwright install chromium
```

### Step 2: Run the Scraper
```powershell
python scraper.py
```
✅ Creates `scraped_data/` with JSON files

### Step 3: Setup Azure (First Time Only)
```powershell
# Login to Azure
az login

# Create Azure AI Search service
az search service create --name techconnect-search --sku standard --location eastus

# Set environment variable
$env:AZURE_SEARCH_ENDPOINT = "https://techconnect-search.search.windows.net"
```

### Step 4: Index to Azure
```powershell
python azure_search_indexer.py
```
✅ Creates index and uploads documents

### Step 5: Test Search
```powershell
python demo.py
```
Choose option 5 to test search functionality

## 📁 Project Files

| File | Purpose |
|------|---------|
| `scraper.py` | Web scraper using Playwright |
| `azure_search_indexer.py` | Azure AI Search integration |
| `demo.py` | Interactive demonstration |
| `rag_example.py` | LLM integration example |
| `scraped_data/` | Output directory with JSON documents |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `AZURE_SETUP.md` | Detailed Azure setup |

## 🔧 Common Commands

### Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux
```

### Run Scraper
```powershell
python scraper.py
```

### Index Documents
```powershell
python azure_search_indexer.py
```

### Run Demo
```powershell
python demo.py
```

### Test Search in Python
```powershell
python
>>> from azure_search_indexer import AzureAISearchManager
>>> manager = AzureAISearchManager("https://your-service.search.windows.net")
>>> results = manager.search("your query")
>>> for r in results: print(r['title'])
```

## 🌐 Customization

### Change Target URLs (scraper.py)
```python
TARGET_URLS = [
    "https://github.com/your-org/repo1",
    "https://github.com/your-org/repo2",
    "https://docs.example.com/page",
]
```

### Add Custom Fields to Index (azure_search_indexer.py)
```python
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="category", type=SearchFieldDataType.String),
    SearchableField(name="tags", type=SearchFieldDataType.String),
    # Add your fields here
]
```

### Adjust Search Results
```python
# Get top 10 results instead of 5
results = manager.search("query", top=10)

# Customize query with filters
results = manager.search(
    search_text="your query",
    search_fields=["title", "content"],  # Only search these fields
    top=5
)
```

## 🤖 Use Cases

### 1. **Chatbot with Company Knowledge**
```python
# User asks question → Search indexed docs → Ground LLM response
response = query_with_rag(rag_system, "How do I implement X?")
```

### 2. **Documentation Search**
Search across multiple repositories with ranking

### 3. **Q&A System**
Answer technical questions based on indexed best practices

### 4. **Code Example Finder**
Index GitHub repos, search for implementation patterns

## ⚠️ Troubleshooting

### Virtual Environment Issues
```powershell
# Recreate venv if packages not found
rm -r venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Azure Authentication Error
```powershell
# Re-login
az login
az account show  # Verify you're logged in
```

### Index Already Exists Error
Delete from Azure Portal or add delete logic to indexer

### Empty Search Results
- Check documents uploaded: `az search service show ...`
- Verify search fields are searchable in index schema
- Check file permissions in `scraped_data/`

## 📚 Learning Resources

- [Playwright Docs](https://playwright.dev/python/)
- [Azure AI Search Docs](https://learn.microsoft.com/azure/search/)
- [RAG Pattern Explanation](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)
- [Python SDK Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents)

## 🚀 Next Steps

1. **Add Semantic Ranking** → Better relevance
2. **Add Vector Embeddings** → Semantic search
3. **Scheduled Updates** → Keep index fresh
4. **Integrate with LLM** → Chat interface
5. **Add Monitoring** → Track usage

## 💡 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    TechConnect3 System                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Input Sources                  Processing                   │
│  ┌────────────────┐          ┌──────────────────┐           │
│  │ GitHub Repos   │          │   Playwright     │           │
│  │ Web Pages      │ ────────→│   Scraper        │           │
│  │ Docs Sites     │          │                  │           │
│  └────────────────┘          └────────┬─────────┘           │
│                                       │                     │
│                                       ▼                     │
│                            ┌──────────────────┐             │
│                            │   Cleaned JSON   │             │
│                            │   Documents      │             │
│                            └────────┬─────────┘             │
│                                      │                      │
│                                      ▼                      │
│         ┌──────────────────────────────────────────┐        │
│         │    Azure AI Search Indexer               │        │
│         │  - Create index with fields             │        │
│         │  - Upload documents                     │        │
│         │  - Configure ranking                    │        │
│         └────────┬─────────────────────────────────┘        │
│                  │                                           │
│                  ▼                                           │
│    ┌──────────────────────────────────────┐                │
│    │  Azure AI Search Service             │                │
│    │  - Indexes documents                 │                │
│    │  - Enables full-text search          │                │
│    │  - Provides REST/Python API          │                │
│    └────────┬─────────────────────────────┘                │
│             │                                               │
│             ▼                                               │
│  ┌────────────────────────────────────┐                    │
│  │    LLM Integration (Optional)      │                    │
│  │  - Search-augmented prompting      │                    │
│  │  - Grounded responses              │                    │
│  │  - Context from indexed data       │                    │
│  └────────────────────────────────────┘                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📞 Support

For issues or questions:
1. Check `README.md` and `AZURE_SETUP.md`
2. Review error messages carefully
3. Check Azure Portal for index status
4. Verify environment variables are set

## 📝 License

MIT

---

**Happy searching! 🔍**

# TechConnect4 - AI Coding Instructions

## Project Overview
TechConnect4 is a **web scraping + Azure AI Search + LLM grounding pipeline** that converts web content into a searchable knowledge base. It's designed for extracting Microsoft Accelerators and GitHub Solution documentation into Azure AI Search indices.

**Core Pipeline**: `scraper.py` → `scraped_data/` (JSON) → `azure_search_indexer.py` → Azure AI Search

## Architecture & Data Flow

### Phase 1: Web Scraping (`scraper.py`)
- **Class**: `AzureAIScraper` - async web scraper using Playwright
- **Key Pattern**: Wait for `networkidle` before extracting (handles JS-heavy pages)
- **Input**: `TARGET_URLS` list of GitHub & Microsoft documentation sites
- **Output**: JSON files in `scraped_data/` with structure:
  ```json
  {
    "source_url": "https://...",
    "title": "Page Title",
    "timestamp": "ISO-8601",
    "content": "cleaned text",
    "metadata": {"char_count": 1234, "word_count": 456}
  }
  ```
- **Important**: HTML is cleaned of `<script>`, `<style>`, `<nav>`, `<footer>`, `<header>` before extraction
- **File naming**: URL segments converted to underscores (e.g., `github_com_microsoft_Solution_Accelerators.json`)

### Phase 2: Azure Indexing (`azure_search_indexer.py`)
- **Class**: `AzureAISearchManager` - manages search index lifecycle
- **Authentication**: Uses API key from `AZURE_SEARCH_API_KEY` env var (not DefaultAzureCredential in this file)
- **Index Fields**: `id` (key), `source_url`, `title`, `content` (analyzed with `en.microsoft`), `timestamp`, `char_count`, `word_count`
- **Workflow**: Create index → load all JSON from `scraped_data/` → upload documents
- **Document ID**: Filename without `.json` extension

### Phase 3: LLM Integration (`rag_example.py`)
- **Pattern**: Retrieval-Augmented Generation (RAG) - search for context, then ground LLM responses
- **Requires**: Azure OpenAI endpoint + search index populated

## Critical Developer Workflows

### Running the Full Pipeline
```powershell
# 1. Activate venv
.\venv\Scripts\Activate.ps1

# 2. Scrape data
python scraper.py          # Creates JSON files in scraped_data/

# 3. Set Azure credentials & endpoint
$env:AZURE_SEARCH_API_KEY = "your-admin-api-key"
$env:AZURE_SEARCH_ENDPOINT = "https://your-service.search.windows.net"

# 4. Index to Azure
python azure_search_indexer.py
```

### Interactive Testing (without Azure setup)
```powershell
python demo.py  # 5-step guided workflow with inline options
```

### Debugging & Validation
- Check `scraped_data/` folder for JSON output after scraping
- `demo.py` → Option 2 shows sample of scraped data
- Test Azure connectivity with quick search before full indexing

## Project-Specific Patterns & Conventions

### JSON Document Format
All scraped documents follow this structure (non-negotiable for indexer):
- Must include: `source_url`, `title`, `content`, `timestamp`, `metadata` (dict with counts)
- Used by `azure_search_indexer.py` to map fields to search index
- If modifying scraper output, update corresponding field mappings in indexer

### Async Pattern in Scraper
- Uses `async_playwright()` context manager
- Each URL gets its own `page` object (created + closed per URL)
- Network wait: `wait_until="networkidle"` is intentional (respects JS rendering)

### Environment-Driven Configuration
- **No hardcoded credentials** - all sensitive data in env vars:
  - `AZURE_SEARCH_ENDPOINT` - search service URL
  - `AZURE_SEARCH_API_KEY` - admin API key (not query key)
  - `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID`, etc. for other services
- `demo.py` prompts for missing values interactively

### Text Cleaning Strategy
- Remove noise: scripts, styles, navigation, headers, footers
- Whitespace normalization: `re.sub(r'\s+', ' ', text)`
- Extract from `<main>` or `<article>` tags first, fallback to `<body>`

## External Dependencies & Integration Points

### Core Libraries
- **playwright** (1.57.0) - Async browser automation for JS rendering
- **beautifulsoup4** (4.14.3) - HTML parsing after page load
- **azure-search-documents** (11.6.0) - Index creation & document upload
- **azure-identity** (1.25.1) - Some modules use DefaultAzureCredential
- **azure-storage-blob** (12.22.0) - Optional blob storage integration

### Azure Services
1. **Azure AI Search** (formerly Cognitive Search) - Full-text search index
2. **Azure OpenAI** (optional) - For `rag_example.py` LLM grounding
3. **Azure Blob Storage** (optional) - Document storage alternative

### Cross-Component Communication
- Scraper → Indexer: Via `scraped_data/` JSON files (file-based contract)
- Indexer → Search: Via Azure REST API (SDK handles HTTP details)
- No inter-component dependencies within the codebase itself

## Key Files & Their Purpose
- **scraper.py** - Web scraping entry point; modify `TARGET_URLS` to add sources
- **azure_search_indexer.py** - Azure integration; modify index schema if adding fields
- **demo.py** - User-friendly workflow; reference for testing without code
- **rag_example.py** - Example RAG pattern for LLM grounding
- **test_search.py** - Search API testing utilities
- **scraped_data/** - Output directory (JSON documents) - **do not commit to git**
- **requirements.txt** - Pinned dependency versions

## Gotchas & Common Issues
1. **Playwright timeout on slow pages**: Increase `timeout=60000` in `scraper.py` if needed
2. **Azure API key vs. search key**: Indexer requires **admin API key**, not query key
3. **Large content truncation**: Ensure JSON field sizes don't exceed Azure limits (~32 MB per doc is safe)
4. **Async context managers**: Scraper cleanup (page/browser closure) is critical for resource management
5. **Search index recreation**: Must delete old index before `create_index()` on schema changes

## Testing & Validation
- Unit tests: Run `test_search.py` for search API validation
- Integration: `demo.py` validates end-to-end workflow interactively
- Manual: Check `scraped_data/` folder structure and sample JSON before indexing

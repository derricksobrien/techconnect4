# Azure AI Search Setup Guide for TechConnect3

## Step 1: Create Azure AI Search Service

### Via Azure Portal (GUI)
1. Go to [Azure Portal](https://portal.azure.com)
2. Click **+ Create a resource**
3. Search for **Azure AI Search**
4. Click **Create**
5. Fill in:
   - **Subscription**: Select your subscription
   - **Resource Group**: Create new (e.g., `rg-techconnect`)
   - **Service Name**: `techconnect-search` (must be globally unique)
   - **Location**: East US (or your preferred region)
   - **Pricing Tier**: Select "Standard" (includes semantic ranking)
6. Click **Review + Create** → **Create**

### Via Azure CLI
```powershell
# Create resource group
az group create --name rg-techconnect --location eastus

# Create Azure AI Search service
az search service create `
  --name techconnect-search `
  --resource-group rg-techconnect `
  --sku standard

# Get the endpoint
$endpoint = az search service show --name techconnect-search `
  --resource-group rg-techconnect --query properties.endpoint -o tsv
```

## Step 2: Set Environment Variables

```powershell
# Set the search endpoint
$env:AZURE_SEARCH_ENDPOINT = "https://techconnect-search.search.windows.net"

# Verify Azure login
az account show
```

## Step 3: Grant Access (if needed)

If you're using a service principal, assign the **Search Index Data Contributor** role:

```powershell
$principalId = "your-app-id"
$resourceId = "/subscriptions/your-sub-id/resourceGroups/rg-techconnect/providers/Microsoft.Search/searchServices/techconnect-search"

az role assignment create `
  --assignee $principalId `
  --role "Search Index Data Contributor" `
  --scope $resourceId
```

## Step 4: Run the Indexer

```powershell
cd c:\Users\derri\Code\TechConnect3

# Activate venv
.\venv\Scripts\Activate.ps1

# Run the indexer
python.exe azure_search_indexer.py
```

Expected output:
```
[*] Creating index...
[+] Index 'techconnect-index' created successfully
[*] Indexing documents...
[+] Loaded: aka_ms_csaGoldStandards
[+] Loaded: github_com_microsoft_Solution_Accelerators
[+] Loaded: github_com_microsoft_Commercial_Solution_Areas_Accelerators
[+] Successfully uploaded 3 documents to index
[*] Testing search...
```

## Step 5: Verify in Azure Portal

1. Go to Azure Portal → Your Search Service
2. Click **Indexes** in the left menu
3. You should see `techconnect-index`
4. Click on it to see the indexed documents

## Step 6: Query Your Index

### Via Python (LLM Grounding)
```python
from azure_search_indexer import AzureAISearchManager

manager = AzureAISearchManager("https://techconnect-search.search.windows.net")

# Search with a natural language query
results = manager.search("accelerator framework best practices", top=5)

for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['source_url']}")
    print(f"Content: {result['content'][:500]}...")
    print("---")
```

### Via Azure Portal (Search Explorer)
1. Go to Search Service → **Search explorer**
2. Select index `techconnect-index`
3. Type a query like: `"solution accelerators"`
4. Click **Search**

### Via REST API (curl)
```powershell
$headers = @{
    "api-key" = "your-admin-key"
    "Content-Type" = "application/json"
}

$body = @{
    search = "accelerator"
    top = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://techconnect-search.search.windows.net/indexes/techconnect-index/docs/search?api-version=2024-09-01-preview" `
  -Headers $headers `
  -Body $body `
  -Method Post
```

## Step 7: Integrate with LLM (Optional)

### With Azure OpenAI
```python
from azure.ai.openai import AzureOpenAI
from azure_search_indexer import AzureAISearchManager

# Initialize clients
search_manager = AzureAISearchManager("https://techconnect-search.search.windows.net")
openai_client = AzureOpenAI(
    api_key="your-openai-key",
    api_version="2024-05-01-preview",
    azure_endpoint="https://your-openai-resource.openai.azure.com"
)

# Search for context
user_query = "How do I build a solution accelerator?"
search_results = search_manager.search(user_query, top=3)

# Build context from search results
context = "\n\n".join([
    f"Source: {r['source_url']}\nTitle: {r['title']}\n{r['content'][:500]}..."
    for r in search_results
])

# Create RAG prompt
system_prompt = f"""You are a helpful assistant that answers questions about Microsoft Solution Accelerators.
Use the following context to answer questions:

{context}"""

# Get response from LLM
response = openai_client.chat.completions.create(
    model="gpt-4-turbo",
    system_prompt=system_prompt,
    messages=[
        {"role": "user", "content": user_query}
    ]
)

print(response.choices[0].message.content)
```

## Troubleshooting

### Error: "Index already exists"
```powershell
# Delete the existing index (you can modify azure_search_indexer.py to add --delete-existing flag)
# Or manually delete from Azure Portal → Indexes → Delete
```

### Error: "Unauthorized access"
```powershell
# Ensure you're logged in
az login

# Check role assignment
az role assignment list --resource-group rg-techconnect
```

### Slow queries
- Add semantic ranking tier (Portal → Pricing tier → Standard with semantic ranking)
- Use vector embeddings for semantic search
- Add more specific filters

### Empty search results
- Verify documents were uploaded: Portal → Index → Documents
- Check if searchable fields are properly configured
- Try simpler queries first

## Cost Optimization

- **Standard Tier**: ~$200-400/month for search
- **Data Storage**: Minimal (depends on content size)
- **Replicas**: Use 1 for dev/test, 2+ for production

To estimate costs:
```powershell
az search service list --resource-group rg-techconnect `
  --query "[].sku.name"
```

## Next Steps

1. **Add Semantic Ranking**: Enable semantic ranking for better relevance
2. **Vector Search**: Add Azure OpenAI embeddings for semantic search
3. **Scheduled Updates**: Set up a timer to re-scrape and update the index
4. **Analytics**: Monitor search performance and user queries
5. **Multi-Index**: Create separate indices for different content types

## Resources

- [Azure AI Search Docs](https://learn.microsoft.com/azure/search/)
- [Search REST API](https://learn.microsoft.com/rest/api/searchservice/)
- [Python SDK](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents)

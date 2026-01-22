# 🎯 AZURE AI SEARCH - CREDENTIALS & QUICK START

## 🔑 Your Credentials (Copy & Save These)

```
SERVICE INSTANCE NAME:
techconnect-search

API ENDPOINT:
https://techconnect-search.search.windows.net

ADMIN API KEY (PRIMARY):
pEvTYOhRCdH41D2i1ALPFDxzBdK6US68ESsrADZa84AzSeDi1Y03

ADMIN API KEY (SECONDARY):
3W49yzZ63XYi2HqPukzM1s3DLLzsPM2SHBIIuHmQCBAzSeAp17rL

INDEX NAME:
techconnect-index

RESOURCE GROUP:
techconnect3
```

---

## ⚡ 30-Second Integration

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

client = SearchClient(
    endpoint="https://techconnect-search.search.windows.net",
    index_name="techconnect-index",
    credential=AzureKeyCredential("pEvTYOhRCdH41D2i1ALPFDxzBdK6US68ESsrADZa84AzSeDi1Y03")
)

# Search your indexed documents
results = client.search(search_text="solution accelerators", top=5)

for result in results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['source_url']}")
    print(f"Content: {result['content'][:200]}...")
```

---

## 📦 Installation

```bash
pip install azure-search-documents azure-core
```

---

## 🧪 Test with curl

```bash
curl -X POST \
  "https://techconnect-search.search.windows.net/indexes/techconnect-index/docs/search?api-version=2024-09-01-preview" \
  -H "api-key: pEvTYOhRCdH41D2i1ALPFDxzBdK6US68ESsrADZa84AzSeDi1Y03" \
  -H "Content-Type: application/json" \
  -d '{"search":"solution accelerators","top":5}'
```

---

## 🤖 Use with LLM (RAG Pattern)

```python
from azure.ai.openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Step 1: Search for context
search = SearchClient(
    endpoint="https://techconnect-search.search.windows.net",
    index_name="techconnect-index",
    credential=AzureKeyCredential("pEvTYOhRCdH41D2i1ALPFDxzBdK6US68ESsrADZa84AzSeDi1Y03")
)

results = list(search.search("your question", top=3))

# Step 2: Build context
context = "\n".join([f"- {r['title']}: {r['content'][:200]}" for r in results])

# Step 3: Send to LLM
llm = AzureOpenAI(
    api_key="your-openai-key",
    api_version="2024-05-01-preview",
    azure_endpoint="https://your-resource.openai.azure.com/"
)

response = llm.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{
        "role": "system",
        "content": f"Use this context: {context}"
    }, {
        "role": "user",
        "content": "your question"
    }]
)

print(response.choices[0].message.content)
```

---

## 📊 What's Indexed (4 Documents)

1. **Microsoft AI Solution Accelerators** (1,381 words)
   - https://accelerators.ms/

2. **GitHub: Solution-Accelerators** (218 words)
   - https://github.com/microsoft/Solution-Accelerators

3. **CSA Gold Standards** (43 words)
   - https://aka.ms/csaGoldStandards

4. **GitHub: Commercial-Solution-Areas** (15 words)
   - https://github.com/microsoft/Commercial-Solution-Areas-Accelerators

---

## ✅ Status

- ✓ Service Created & Running
- ✓ Index: `techconnect-index`
- ✓ Documents: 4 (1,657 total words)
- ✓ Search: Working
- ✓ RAG Ready: Yes

---

## 🔒 Environment Setup (Recommended)

```powershell
# PowerShell
$env:AZURE_SEARCH_ENDPOINT = "https://techconnect-search.search.windows.net"
$env:AZURE_SEARCH_API_KEY = "pEvTYOhRCdH41D2i1ALPFDxzBdK6US68ESsrADZa84AzSeDi1Y03"
$env:AZURE_OPENAI_ENDPOINT = "your-endpoint"
$env:AZURE_OPENAI_API_KEY = "your-key"
```

Or create `.env` file:
```
AZURE_SEARCH_ENDPOINT=https://techconnect-search.search.windows.net
AZURE_SEARCH_API_KEY=pEvTYOhRCdH41D2i1ALPFDxzBdK6US68ESsrADZa84AzSeDi1Y03
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_KEY=your-key
```

---

## 🎯 Common Tasks

### Search
```python
results = client.search("your query", top=10)
```

### Filter
```python
results = client.search("query", filter="word_count gt 100")
```

### Get Specific Fields
```python
results = client.search("query", select=["title", "source_url"])
```

### Sort by Relevance
```python
results = client.search("query", top=5)  # Default is by relevance
```

---

## 🔗 Quick Links

- **Azure Portal**: https://portal.azure.com
- **Search Service**: https://techconnect-search.search.windows.net
- **Python SDK**: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search
- **REST API Docs**: https://learn.microsoft.com/rest/api/searchservice/
- **RAG Pattern**: https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview

---

## 🚀 Next Steps

1. **Use These Credentials** in your RAG application
2. **Read** `AI_SEARCH_CREDENTIALS.md` for detailed examples
3. **Integrate** with Azure OpenAI or your preferred LLM
4. **Test** with the code samples above
5. **Deploy** to production when ready

---

**Ready to build with RAG!** 🎉

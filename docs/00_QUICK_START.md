# Quick Start: Using Your AI Foundry Agent

## Your Agent is Ready! 🎉

**Agent ID**: `asst_rFwMHjHtgDeQ1TprE6IEFzOh`  
**Name**: `SolutionAccelerators-Assistant`  
**Model**: `gpt-4o`  
**Status**: ✅ **READY TO USE**

---

## Test It Right Now (3 Steps)

### Step 1: Go to AI Foundry Portal
- Visit: https://ai.azure.com
- Project: **admin-1994**
- Agent: **SolutionAccelerators-Assistant**

### Step 2: Add Your Knowledge Files
1. Click **Files** or **Knowledge** section
2. Click **Upload**
3. Select these 4 files from `knowledge_sources/` folder:
   - `accelerators_ms_.md`
   - `aka_ms_csaGoldStandards.md`
   - `github_com_microsoft_Commercial_Solution_Areas_Accelerators.md`
   - `github_com_microsoft_Solution_Accelerators.md`
4. AI Foundry auto-chunks them (2-3 minutes)

### Step 3: Test Queries
Click **Test** or **Chat** and ask:
- "What are Microsoft Solution Accelerators?"
- "Tell me about the GitHub repos in your knowledge"
- "What enterprise cloud solutions do you have?"

---

## Use in Code

### Option A: Azure OpenAI SDK (Simplest)
```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-10-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://dcsinstance.openai.azure.com/")
)

response = client.chat.completions.create(
    model="gpt4-1",
    messages=[{"role": "user", "content": "Query here"}]
)
print(response.choices[0].message.content)
```

### Option B: AI Foundry SDK (Advanced)
```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

client = AIProjectClient(
    endpoint="https://admin-1994-resource.services.ai.azure.com/api/projects/admin-1994",
    credential=DefaultAzureCredential()
)

# Use client.agents for direct agent management
```

### Option C: REST API (Raw Control)
```powershell
$headers = @{
    "api-key" = $env:AZURE_FOUNDRY_KEY
    "Content-Type" = "application/json"
}

$endpoint = $env:AZURE_FOUNDRY_ENDPOINT

Invoke-RestMethod -Uri "$endpoint/agents" -Headers $headers -Method GET
```

---

## Test Scripts Included

Ready to run:
```bash
# Convert scraped JSON to markdown
python json_to_markdown_converter.py

# Create agent (already done - shows what ran)
python stage2_foundry_sdk.py

# Test agent functionality
python stage3_test_openai.py
```

---

## Credentials Reference

**AI Foundry**
```
Endpoint: https://admin-1994-resource.services.ai.azure.com/api/projects/admin-1994
Key: [REDACTED - Set AZURE_FOUNDRY_KEY environment variable]
```

**Azure OpenAI** (for calling gpt-4o)
```
Endpoint: https://dcsinstance.openai.azure.com/
Key: [REDACTED - Set AZURE_OPENAI_API_KEY environment variable]
Deployment: gpt4-1
```

---

## Architecture

```
Your Data
  ↓
scraped_data/*.json (from web scraper)
  ↓
json_to_markdown_converter.py
  ↓
knowledge_sources/*.md (4 files ready for upload)
  ↓
[Manual Upload via Portal UI] ← YOU ARE HERE
  ↓
AI Foundry Agent (asst_rFwMHjHtgDeQ1TprE6IEFzOh)
  ↓
Automatic Chunking + Vectorization
  ↓
File Search Tool Enabled ✓
  ↓
Ready for Queries!
```

---

## What to Do Next

1. **Upload knowledge files** (5 min) - via AI Foundry portal
2. **Test with queries** (2 min) - verify it works
3. **Integrate in your app** - use REST API or SDKs above
4. **Optional: Automate** - future work on file upload API

---

## Comparison: What Changed from Original Plan

| Original Plan | Current Solution |
|---|---|
| Web Scraper → JSON | ✅ Web Scraper → JSON |
| Index to Azure Search | → AI Foundry Agent (simpler) |
| Custom RAG pipeline | → Built-in File Search Tool |
| Manual chunking | → Automatic (portal) |
| Complex indexing | → One-click upload |

**Result**: Same goal, simpler implementation (like Skillable!)

---

## Support & Troubleshooting

**If agent not responding:**
- Check files are uploaded (should see checksums in portal)
- Wait 2-3 minutes after upload for indexing
- Try different query phrasing

**If upload fails:**
- Files must be text-based (markdown works)
- Size limit: individual files under 100MB
- Check API permissions in portal

**If credentials wrong:**
- Copy from Azure Portal → admin-1994-resource → Keys & Endpoint
- Make sure you're using Foundry key, not OpenAI key

---

**Agent Ready**: `asst_rFwMHjHtgDeQ1TprE6IEFzOh` ✅

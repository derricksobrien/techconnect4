# Azure OpenAI Quota Increase Request Guide

## Quick Summary
Your subscription needs quota for GPT-3.5-turbo or GPT-4 deployments in the eastus region.

---

## Method 1: Azure Portal (Recommended - Fastest)

### Step 1: Open Azure Portal
1. Go to https://portal.azure.com
2. Sign in with your Azure account

### Step 2: Navigate to Quotas
1. Search for **"Quotas"** in the search bar at the top
2. Click on **"Quotas"** (under Services)
3. Filter by:
   - **Provider**: Cognitive Services
   - **Region**: East US

### Step 3: Find OpenAI Quotas
Look for entries like:
- `Cognitive Services - OpenAI Deployments (gpt-35-turbo) - East US`
- `Cognitive Services - OpenAI Deployments (gpt-4) - East US`

### Step 4: Request Increase
1. Click the checkbox next to the quota you need
2. Click **"Request quota increase"** button
3. Fill in the form:
   - **New limit**: Enter desired value (e.g., `1` for testing)
   - **Description**: "Deploying Azure OpenAI GPT-3.5-turbo for TechConnect4 application"
4. Click **Submit**

### Step 5: Wait for Approval
- **Timeline**: Usually 1-2 business days
- **Notification**: You'll receive an email when approved
- **No email?** Check the Quotas page for status

---

## Method 2: Support Request (If Quota Page Doesn't Work)

### Step 1: Create Support Ticket
1. Go to https://portal.azure.com
2. Search for **"Help + support"**
3. Click **"Create a support request"**

### Step 2: Fill Support Form
- **Issue type**: `Service and subscription limits (quotas)`
- **Service**: `Cognitive Services`
- **Quota type**: `OpenAI - East US`
- **Details**:
  ```
  I need to deploy GPT-3.5-turbo (or GPT-4) in East US region.
  Account: techconnect-aoai
  Resource Group: techconnect-rg
  Requested quota: 1 (for testing/development)
  
  Error encountered:
  "The specified SKU 'Standard' for model 'gpt-35-turbo 1106' 
   is not supported in this region 'eastus'"
  ```
- **Severity**: `Low` (not blocking critical service)
4. Click **Submit**

---

## Method 3: Azure CLI (Alternative)

Run this PowerShell command to check current quota:

```powershell
az provider register --namespace Microsoft.CognitiveServices
az quota show --resource-name "Cognitive Services - OpenAI Deployments (gpt-35-turbo) - East US" `
  --scope "/subscriptions/7ee5516b-974e-44ba-96a6-e2dd381dc83c"
```

*(Note: CLI quota requests are more limited; Portal is recommended)*

---

## What to Request

Choose ONE of these based on your needs:

| Model | Why | Recommended |
|-------|-----|-------------|
| **gpt-35-turbo** | Cheaper, faster, good for demos | ✅ Start here |
| **gpt-4** | More capable, better reasoning | Use if approved |
| **Both** | Maximum flexibility | Best option |

---

## After Approval

Once quota is approved (you'll get an email):

1. Run this command to verify:
```powershell
az cognitiveservices account deployment create `
  --name techconnect-aoai `
  --resource-group techconnect-rg `
  --deployment-name gpt35-turbo `
  --model-name gpt-35-turbo `
  --model-version 1106 `
  --model-format OpenAI `
  --sku-capacity 1 `
  --sku standard
```

2. Test the deployment works (we'll do this once quota is approved)

---

## Timeline

| Action | Timeline |
|--------|----------|
| Submit request | Immediate |
| Azure review | 1-2 business days |
| Approval email | Sent to your account email |
| Deployment available | Immediately after approval |

---

## Contact Information

- **Azure Support**: Support Portal > Help + support > Create a support request
- **Quota help**: Search "Quotas" in portal for visual interface
- **Status tracking**: Quotas page shows real-time status

---

## Notes

- Your **subscription ID**: `7ee5516b-974e-44ba-96a6-e2dd381dc83c`
- Your **resource group**: `techconnect-rg`
- Your **AOAI account**: `techconnect-aoai`
- **Region**: `eastus` (East US)

Save these for your quota request!

# ============================================================================
# Azure OpenAI Setup Script for TechConnect4
# Creates minimal AOAI endpoint with GPT-4 and tests connectivity
# ============================================================================

param(
    [string]$ResourceGroup = "techconnect-rg",
    [string]$Location = "eastus",
    [string]$AccountName = "techconnect-aoai",
    [string]$DeploymentName = "gpt4-turbo"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Azure OpenAI Setup for TechConnect4" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Check Azure CLI authentication
Write-Host "[1/6] Checking Azure authentication..." -ForegroundColor Yellow
try {
    $account = az account show --query "user.name" -o tsv 2>$null
    if ($account) {
        Write-Host "✓ Authenticated as: $account`n" -ForegroundColor Green
    } else {
        throw "Not authenticated"
    }
} catch {
    Write-Host "✗ Not authenticated. Running 'az login'..." -ForegroundColor Red
    az login
    Write-Host ""
}

# Step 2: Create Resource Group
Write-Host "[2/6] Creating resource group '$ResourceGroup' in '$Location'..." -ForegroundColor Yellow
try {
    $rg = az group create --name $ResourceGroup --location $Location --query "id" -o tsv
    Write-Host "✓ Resource group created: $rg`n" -ForegroundColor Green
} catch {
    Write-Host "✗ Error creating resource group: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Create Azure OpenAI Account
Write-Host "[3/6] Creating Azure OpenAI account '$AccountName'..." -ForegroundColor Yellow
try {
    $aoai = az cognitiveservices account create `
        --name $AccountName `
        --resource-group $ResourceGroup `
        --kind OpenAI `
        --sku s0 `
        --location $Location `
        --yes `
        --query "id" -o tsv
    Write-Host "✓ AOAI account created: $aoai`n" -ForegroundColor Green
    Start-Sleep -Seconds 5  # Wait for account to stabilize
} catch {
    Write-Host "⚠ Account may already exist or error occurred: $_" -ForegroundColor Yellow
}

# Step 4: Create Deployment (GPT-4 Turbo)
Write-Host "[4/6] Creating GPT-4 Turbo deployment '$DeploymentName'..." -ForegroundColor Yellow
try {
    $deployment = az cognitiveservices account deployment create `
        --name $AccountName `
        --resource-group $ResourceGroup `
        --deployment-name $DeploymentName `
        --model-name gpt-4-turbo `
        --model-version 2024-04-09 `
        --sku-capacity 1 `
        --sku standard `
        --query "id" -o tsv
    Write-Host "✓ Deployment created: $deployment`n" -ForegroundColor Green
    Start-Sleep -Seconds 3
} catch {
    Write-Host "⚠ Deployment may already exist or error occurred: $_" -ForegroundColor Yellow
}

# Step 5: Retrieve Credentials
Write-Host "[5/6] Retrieving credentials..." -ForegroundColor Yellow
try {
    $endpoint = az cognitiveservices account show `
        --name $AccountName `
        --resource-group $ResourceGroup `
        --query "properties.endpoint" -o tsv
    
    $apiKey = az cognitiveservices account keys list `
        --name $AccountName `
        --resource-group $ResourceGroup `
        --query "key1" -o tsv
    
    $subscriptionId = az account show --query "id" -o tsv
    
    Write-Host "✓ Credentials retrieved`n" -ForegroundColor Green
    
    # Display credentials for Skillable configuration
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SKILLABLE CONFIGURATION DETAILS" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green
    
    Write-Host "API URL:" -ForegroundColor Cyan
    Write-Host $endpoint -ForegroundColor White
    Write-Host ""
    
    Write-Host "API Key (first 20 chars): $($apiKey.Substring(0, 20))..." -ForegroundColor Cyan
    Write-Host "Full Key (copy entire value):" -ForegroundColor Cyan
    Write-Host $apiKey -ForegroundColor White
    Write-Host ""
    
    Write-Host "Instance Name:" -ForegroundColor Cyan
    Write-Host $AccountName -ForegroundColor White
    Write-Host ""
    
    Write-Host "Deployment Name:" -ForegroundColor Cyan
    Write-Host $DeploymentName -ForegroundColor White
    Write-Host ""
    
    Write-Host "Model Type:" -ForegroundColor Cyan
    Write-Host "GPT-4 Turbo" -ForegroundColor White
    Write-Host ""
    
    Write-Host "API Authorization Method:" -ForegroundColor Cyan
    Write-Host "API Key Header" -ForegroundColor White
    Write-Host ""
    
    Write-Host "API Key Header Name:" -ForegroundColor Cyan
    Write-Host "api-key" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Resource Group:" -ForegroundColor Cyan
    Write-Host $ResourceGroup -ForegroundColor White
    Write-Host ""
    
    Write-Host "Subscription ID:" -ForegroundColor Cyan
    Write-Host $subscriptionId -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "✗ Error retrieving credentials: $_" -ForegroundColor Red
    exit 1
}

# Step 6: Test Connectivity
Write-Host "[6/6] Testing API connectivity..." -ForegroundColor Yellow
try {
    $headers = @{
        "api-key" = $apiKey
        "Content-Type" = "application/json"
    }
    
    $body = @{
        messages = @(
            @{
                role = "user"
                content = "Say 'TechConnect4 is ready!' in one sentence."
            }
        )
        max_tokens = 100
    } | ConvertTo-Json
    
    $apiUrlWithPath = "$endpoint/openai/deployments/$DeploymentName/chat/completions?api-version=2024-02-15-preview"
    
    $response = Invoke-RestMethod -Uri $apiUrlWithPath `
        -Method Post `
        -Headers $headers `
        -Body $body
    
    $message = $response.choices[0].message.content
    Write-Host "✓ API Test Successful!`n" -ForegroundColor Green
    Write-Host "Model Response: $message`n" -ForegroundColor Green
    
} catch {
    Write-Host "⚠ API test failed (may need time to initialize): $_`n" -ForegroundColor Yellow
}

# Save credentials to file for reference
$credFile = "$(Get-Location)\AOAI_CREDENTIALS.txt"
@"
========================================
AZURE OPENAI CREDENTIALS - $(Get-Date)
========================================

ENDPOINT:
$endpoint

API KEY:
$apiKey

INSTANCE NAME:
$AccountName

DEPLOYMENT NAME:
$DeploymentName

MODEL TYPE:
GPT-4 Turbo

API AUTHORIZATION:
Method: API Key Header
Header Name: api-key

RESOURCE GROUP:
$ResourceGroup

SUBSCRIPTION ID:
$subscriptionId

========================================
To use in your code:
========================================

# PowerShell Environment Variables
`$env:AZURE_OPENAI_ENDPOINT = "$endpoint"
`$env:AZURE_OPENAI_API_KEY = "$apiKey"
`$env:AZURE_OPENAI_DEPLOYMENT_NAME = "$DeploymentName"

# Or in Python
import os
os.environ['AZURE_OPENAI_ENDPOINT'] = "$endpoint"
os.environ['AZURE_OPENAI_API_KEY'] = "$apiKey"
os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'] = "$DeploymentName"
"@ | Out-File -FilePath $credFile -Encoding UTF8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ SETUP COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Credentials saved to: $credFile`n" -ForegroundColor Green

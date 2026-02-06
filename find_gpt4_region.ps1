# Find which Azure region supports GPT-4
# Tests multiple regions for model availability

$regions = @(
    "eastus",
    "westus",
    "westus2",
    "northcentralus",
    "southcentralus",
    "eastus2",
    "canadacentral",
    "swedencentral",
    "uksouth",
    "westeurope",
    "franccentral",
    "australiaeast"
)

$resourceGroup = "techconnect-rg"

Write-Host "Testing GPT-4 availability across Azure regions..." -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$supportedRegions = @()

foreach ($region in $regions) {
    Write-Host "Testing region: $region..." -ForegroundColor Yellow
    
    # Try to create deployment in this region
    try {
        $result = az cognitiveservices account deployment create `
            --name techconnect-aoai `
            --resource-group $resourceGroup `
            --deployment-name "test-gpt4-$region" `
            --model-name "gpt-4" `
            --model-version "turbo-2024-04-09" `
            --model-format "OpenAI" `
            --sku-capacity 1 `
            --sku "standard" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ GPT-4 SUPPORTED in $region" -ForegroundColor Green
            $supportedRegions += $region
        } else {
            # Check error message
            $errorMsg = $result -join " "
            if ($errorMsg -match "not supported" -or $errorMsg -match "invalid") {
                Write-Host "  ✗ GPT-4 not supported" -ForegroundColor Red
            } else {
                Write-Host "  ? Error: $($errorMsg.Substring(0, 80))..." -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "  ✗ Error testing region" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Results:" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

if ($supportedRegions.Count -gt 0) {
    Write-Host "Regions that support GPT-4:" -ForegroundColor Green
    foreach ($region in $supportedRegions) {
        Write-Host "  • $region" -ForegroundColor Green
    }
} else {
    Write-Host "No regions tested supported GPT-4 with that configuration." -ForegroundColor Yellow
    Write-Host "Trying GPT-3.5-turbo instead..." -ForegroundColor Yellow
    
    foreach ($region in $regions) {
        Write-Host "Testing $region for GPT-3.5..." -ForegroundColor Yellow
        
        try {
            $result = az cognitiveservices account deployment create `
                --name techconnect-aoai `
                --resource-group $resourceGroup `
                --deployment-name "test-gpt35-$region" `
                --model-name "gpt-35-turbo" `
                --model-version "1106" `
                --model-format "OpenAI" `
                --sku-capacity 1 `
                --sku "standard" 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✓ GPT-3.5-turbo SUPPORTED in $region" -ForegroundColor Green
                $supportedRegions += $region
            }
        } catch {
            # Silent continue
        }
    }
}

if ($supportedRegions.Count -gt 0) {
    Write-Host "`nRecommended region: $($supportedRegions[0])" -ForegroundColor Green
} else {
    Write-Host "`nNo models found. Check Azure OpenAI availability in your subscription." -ForegroundColor Red
}

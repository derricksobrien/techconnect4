@echo off
REM TechConnect3 - Setup and Run Script
REM Run this batch file to set up and use the project

setlocal enabledelayedexpansion

echo.
echo ========================================
echo TechConnect3 - Setup Script
echo ========================================
echo.

:menu
echo.
echo Choose an option:
echo   1. Setup Virtual Environment (first time only)
echo   2. Run Scraper
echo   3. Index to Azure AI Search
echo   4. Run Interactive Demo
echo   5. Open Python Shell for Testing
echo   6. View Scraped Data
echo   0. Exit
echo.

set /p choice="Enter your choice (0-6): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto scrape
if "%choice%"=="3" goto index
if "%choice%"=="4" goto demo
if "%choice%"=="5" goto shell
if "%choice%"=="6" goto view
if "%choice%"=="0" goto exit
goto invalid

:setup
echo.
echo [*] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [!] Failed to create venv
    goto menu
)

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [!] Failed to install dependencies
    goto menu
)

echo [*] Installing Playwright browsers...
python -m playwright install chromium
if errorlevel 1 (
    echo [!] Failed to install Playwright
    goto menu
)

echo.
echo [+] Setup complete!
echo [+] Virtual environment is active
echo.
echo Next steps:
echo   1. Set Azure Search endpoint: 
echo      $env:AZURE_SEARCH_ENDPOINT = 'https://your-service.search.windows.net'
echo   2. Run scraper: python scraper.py
echo   3. Index to Azure: python azure_search_indexer.py
echo.
goto menu

:scrape
echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Running scraper...
python scraper.py
echo.
goto menu

:index
echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

if not defined AZURE_SEARCH_ENDPOINT (
    echo [!] AZURE_SEARCH_ENDPOINT not set!
    echo [*] Set it with:
    echo    set AZURE_SEARCH_ENDPOINT=https://your-service.search.windows.net
    goto menu
)

echo [*] Indexing to Azure AI Search...
echo [*] Endpoint: %AZURE_SEARCH_ENDPOINT%
python azure_search_indexer.py
echo.
goto menu

:demo
echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Running demo...
python demo.py
echo.
goto menu

:shell
echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Starting Python shell...
echo.
echo Usage examples:
echo   from azure_search_indexer import AzureAISearchManager
echo   manager = AzureAISearchManager("https://your-service.search.windows.net")
echo   results = manager.search("your query")
echo.
python
echo.
goto menu

:view
echo.
if not exist scraped_data (
    echo [!] No scraped data found
    echo [*] Run the scraper first: python scraper.py
    goto menu
)

echo [+] Scraped data files:
dir scraped_data\*.json
echo.
echo [*] Showing content of first file:
for /f %%f in ('dir /b scraped_data\*.json ^| findstr /r ".*"') do (
    type scraped_data\%%f
    goto menu
)
goto menu

:invalid
echo.
echo [!] Invalid choice
echo.
goto menu

:exit
echo.
echo [*] Goodbye!
echo.
exit /b 0

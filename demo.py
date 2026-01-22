#!/usr/bin/env python3
"""
TechConnect3 Demo - End-to-end workflow
Demonstrates scraping, indexing, and querying with Azure AI Search
"""

import os
import sys
import json
from pathlib import Path

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def demo_1_scrape_data():
    """Demo 1: Run the web scraper."""
    print_header("DEMO 1: Web Scraping with Playwright")
    
    print("This step will:")
    print("  1. Navigate to target URLs (GitHub, Microsoft Docs)")
    print("  2. Wait for JavaScript to load (networkidle)")
    print("  3. Extract text content and metadata")
    print("  4. Save as JSON files in 'scraped_data/' directory")
    print()
    
    response = input("Run scraper now? (y/n): ").lower()
    if response == 'y':
        print("[*] Starting scraper...")
        import asyncio
        from scraper import AzureAIScraper
        
        scraper = AzureAIScraper()
        try:
            results = asyncio.run(scraper.run())
            completed = len([r for r in results if r is not None])
            print(f"\n[+] Scraping complete! {completed} pages successfully scraped.")
            
            # Show file sizes
            data_dir = Path("scraped_data")
            if data_dir.exists():
                print("\n[+] Files created:")
                for json_file in sorted(data_dir.glob("*.json")):
                    size_kb = json_file.stat().st_size / 1024
                    print(f"    - {json_file.name} ({size_kb:.1f} KB)")
        except Exception as e:
            print(f"[!] Scraper failed: {e}")
            return False
    
    return True

def demo_2_show_scraped_data():
    """Demo 2: Show sample of scraped data."""
    print_header("DEMO 2: Scraped Data Sample")
    
    data_dir = Path("scraped_data")
    json_files = list(data_dir.glob("*.json"))
    
    if not json_files:
        print("[!] No scraped data found. Run Demo 1 first.")
        return False
    
    print(f"[+] Found {len(json_files)} scraped documents:\n")
    
    for json_file in sorted(json_files):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        title = data.get('title', 'No Title')
        url = data.get('source_url', 'No URL')
        content_preview = data.get('content', '')[:100] + "..."
        word_count = data.get('metadata', {}).get('word_count', 0)
        
        print(f"📄 {title}")
        print(f"   URL: {url}")
        print(f"   Words: {word_count}")
        print(f"   Preview: {content_preview}")
        print()
    
    return True

def demo_3_azure_setup():
    """Demo 3: Show Azure setup requirements."""
    print_header("DEMO 3: Azure AI Search Setup")
    
    print("To use Azure AI Search, you need:")
    print()
    print("1. Azure Subscription")
    print("2. Azure AI Search Service (Standard tier recommended)")
    print("3. Azure CLI logged in: 'az login'")
    print()
    
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    
    if endpoint:
        print(f"✅ AZURE_SEARCH_ENDPOINT is set:")
        print(f"   {endpoint}")
        print()
        return True
    else:
        print("❌ AZURE_SEARCH_ENDPOINT not set")
        print()
        print("To set it up:")
        print("1. Create Azure AI Search service (see AZURE_SETUP.md)")
        print("2. Set environment variable:")
        print("   $env:AZURE_SEARCH_ENDPOINT = 'https://your-service.search.windows.net'")
        print()
        print("Quick setup with Azure CLI:")
        print("   az search service create --name techconnect-search --sku standard")
        print()
        return False

def demo_4_index_documents():
    """Demo 4: Index documents to Azure AI Search."""
    print_header("DEMO 4: Indexing to Azure AI Search")
    
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    
    if not endpoint or "<your-service>" in endpoint:
        print("[!] Azure Search endpoint not configured.")
        print("    See Demo 3 or AZURE_SETUP.md for setup instructions")
        return False
    
    print(f"[*] Using Azure Search: {endpoint}")
    print()
    print("This step will:")
    print("  1. Create a search index with fields for content")
    print("  2. Upload all documents from scraped_data/")
    print("  3. Make content searchable")
    print()
    
    response = input("Create index and upload documents? (y/n): ").lower()
    if response == 'y':
        print("[*] Starting indexing...")
        try:
            from azure_search_indexer import AzureAISearchManager
            
            manager = AzureAISearchManager(endpoint)
            
            print("[*] Creating index...")
            manager.create_index()
            
            print("[*] Indexing documents...")
            manager.index_documents()
            
            print("\n[+] Indexing complete!")
            print("\nYou can now:")
            print("  1. Search via Azure Portal")
            print("  2. Use manager.search() in Python")
            print("  3. Integrate with LLM for RAG (Retrieval-Augmented Generation)")
            
            return True
        
        except Exception as e:
            print(f"[!] Indexing failed: {e}")
            print("\nTroubleshooting:")
            print("  - Check Azure CLI login: az login")
            print("  - Verify endpoint is correct")
            print("  - Check role assignments")
            return False
    
    return False

def demo_5_search_and_rag():
    """Demo 5: Search and RAG demonstration."""
    print_header("DEMO 5: Search & LLM Grounding")
    
    endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    
    if not endpoint or "<your-service>" in endpoint:
        print("[!] Azure Search not configured.")
        return False
    
    try:
        from azure_search_indexer import AzureAISearchManager
        
        manager = AzureAISearchManager(endpoint)
        
        print("Example queries you can try:")
        print("  - 'solution accelerators'")
        print("  - 'best practices'")
        print("  - 'cloud architecture'")
        print()
        
        query = input("Enter search query (or press Enter to skip): ").strip()
        
        if query:
            print(f"\n[*] Searching for: '{query}'")
            results = list(manager.search(query, top=3))
            
            if results:
                print(f"\n[+] Found {len(results)} results:\n")
                
                for i, result in enumerate(results, 1):
                    print(f"{i}. {result.get('title', 'No Title')}")
                    print(f"   URL: {result.get('source_url', 'No URL')}")
                    content = result.get('content', '')[:200]
                    print(f"   Content: {content}...")
                    print()
                
                # Show how to use for LLM grounding
                print("For LLM grounding, you would:")
                print("  1. Take these search results")
                print("  2. Build a context string")
                print("  3. Pass to your LLM as background knowledge")
                print("  4. Ask questions grounded in your data")
                
                return True
            else:
                print("[!] No results found")
                return False
    
    except Exception as e:
        print(f"[!] Search failed: {e}")
        return False

def main():
    """Run the demonstration."""
    print("\n")
    print("🚀 TechConnect3 - Azure AI Search + LLM Grounding")
    print("=" * 70)
    print()
    print("This demo will walk you through:")
    print("  1. Scraping GitHub repos and documentation")
    print("  2. Preparing data for Azure AI Search")
    print("  3. Indexing documents to Azure")
    print("  4. Searching and grounding LLM responses")
    print()
    
    demos = [
        ("1", "Scrape Data", demo_1_scrape_data),
        ("2", "View Scraped Data", demo_2_show_scraped_data),
        ("3", "Azure Setup Check", demo_3_azure_setup),
        ("4", "Index to Azure AI Search", demo_4_index_documents),
        ("5", "Search & RAG Demo", demo_5_search_and_rag),
    ]
    
    while True:
        print("\nChoose a demo to run:")
        for key, name, _ in demos:
            print(f"  {key}. {name}")
        print("  0. Exit")
        print()
        
        choice = input("Enter choice (0-5): ").strip()
        
        if choice == "0":
            print("\n[*] Goodbye!")
            break
        
        for key, name, func in demos:
            if choice == key:
                try:
                    success = func()
                    if success is False:
                        print("\n[!] Demo incomplete - some steps failed")
                except KeyboardInterrupt:
                    print("\n\n[*] Demo cancelled by user")
                except Exception as e:
                    print(f"\n[!] Unexpected error: {e}")
                    import traceback
                    traceback.print_exc()
                break
        else:
            if choice != "0":
                print("[!] Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Exiting...")
        sys.exit(0)

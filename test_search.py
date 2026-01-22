#!/usr/bin/env python3
"""Test Azure AI Search indexing"""

import os
from azure_search_indexer import AzureAISearchManager

# Get credentials from environment
endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
api_key = os.getenv('AZURE_SEARCH_API_KEY')

if not endpoint or not api_key:
    print("[!] Missing credentials")
    exit(1)

# Connect to search
manager = AzureAISearchManager(endpoint, api_key=api_key)

# Test search
print("[*] Testing search...")
results = list(manager.search('solution accelerators', top=5))

print(f"\n[+] Found {len(results)} results\n")
for i, r in enumerate(results, 1):
    print(f"{i}. {r.get('title', 'No Title')}")
    print(f"   URL: {r.get('source_url', 'No URL')}")
    print(f"   Words: {r.get('word_count', 0)}")
    print()

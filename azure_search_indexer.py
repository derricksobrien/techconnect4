import os
import json
import glob
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    SearchIndexerIndexProjectionSelector,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
)

class AzureAISearchManager:
    def __init__(self, service_endpoint: str, api_key: str = None, index_name: str = "techconnect-index"):
        """
        Initialize Azure AI Search manager.
        
        Args:
            service_endpoint: Azure Search service endpoint (e.g., https://myservice.search.windows.net)
            api_key: Admin API key (optional, will use env var if not provided)
            index_name: Name of the search index
        """
        self.service_endpoint = service_endpoint
        self.index_name = index_name
        
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.getenv("AZURE_SEARCH_API_KEY")
        
        if not self.api_key:
            raise ValueError("API key must be provided or set in AZURE_SEARCH_API_KEY environment variable")
        
        # Create credential object
        credential = AzureKeyCredential(self.api_key)
        
        # Create clients using API key
        self.index_client = SearchIndexClient(endpoint=service_endpoint, credential=credential)
        self.search_client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)
    
    def create_index(self):
        """Create the search index with fields for scraped content."""
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="source_url", type=SearchFieldDataType.String),
            SearchableField(name="title", type=SearchFieldDataType.String),
            SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.microsoft"),
            SimpleField(name="timestamp", type=SearchFieldDataType.String),
            SimpleField(name="char_count", type=SearchFieldDataType.Int32),
            SimpleField(name="word_count", type=SearchFieldDataType.Int32),
        ]
        
        index = SearchIndex(name=self.index_name, fields=fields)
        
        try:
            result = self.index_client.create_index(index)
            print(f"[+] Index '{self.index_name}' created successfully")
            return result
        except Exception as e:
            print(f"[!] Error creating index: {str(e)}")
            raise
    
    def index_documents(self, data_dir: str = "scraped_data"):
        """
        Index documents from scraped JSON files.
        
        Args:
            data_dir: Directory containing scraped JSON files
        """
        documents = []
        
        # Find all JSON files in the data directory
        json_files = glob.glob(os.path.join(data_dir, "*.json"))
        
        if not json_files:
            print(f"[!] No JSON files found in {data_dir}")
            return
        
        print(f"[*] Found {len(json_files)} files to index")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Create document with Azure Search compatible format
                document = {
                    "id": os.path.basename(json_file).replace('.json', ''),
                    "source_url": data.get("source_url", ""),
                    "title": data.get("title", ""),
                    "content": data.get("content", ""),
                    "timestamp": data.get("timestamp", ""),
                    "char_count": data.get("metadata", {}).get("char_count", 0),
                    "word_count": data.get("metadata", {}).get("word_count", 0),
                }
                documents.append(document)
                print(f"[+] Loaded: {document['id']}")
            
            except Exception as e:
                print(f"[!] Error loading {json_file}: {str(e)}")
        
        if documents:
            try:
                result = self.search_client.upload_documents(documents)
                print(f"[+] Successfully uploaded {len(documents)} documents to index")
                return result
            except Exception as e:
                print(f"[!] Error uploading documents: {str(e)}")
                raise
    
    def search(self, query: str, top: int = 5):
        """
        Search the index.
        
        Args:
            query: Search query string
            top: Number of results to return
            
        Returns:
            Search results
        """
        try:
            results = self.search_client.search(search_text=query, top=top)
            return results
        except Exception as e:
            print(f"[!] Error searching: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage - set these environment variables or hardcode for testing
    service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "https://<your-service>.search.windows.net")
    
    if "<your-service>" in service_endpoint:
        print("[!] Please set AZURE_SEARCH_ENDPOINT environment variable")
        print("    Example: $env:AZURE_SEARCH_ENDPOINT = 'https://myservice.search.windows.net'")
        exit(1)
    
    # Get API key
    api_key = os.getenv("AZURE_SEARCH_API_KEY")
    if not api_key:
        print("[!] Please set AZURE_SEARCH_API_KEY environment variable")
        print("    Get it from Azure Portal or: az search admin-key show --service-name techconnect-search --resource-group techconnect3")
        exit(1)
    
    try:
        manager = AzureAISearchManager(service_endpoint, api_key=api_key)
        
        # Create index
        print("[*] Creating index...")
        manager.create_index()
        
        # Index documents from scraped data
        print("[*] Indexing documents...")
        manager.index_documents()
        
        # Example search
        print("[*] Testing search...")
        results = manager.search("Azure Solution", top=3)
        for result in results:
            print(f"  - {result['title']}: {result['source_url']}")
    
    except Exception as e:
        print(f"[!] Setup failed: {str(e)}")
        import traceback
        traceback.print_exc()

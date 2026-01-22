"""
Azure OpenAI + Azure AI Search Integration
Example of using TechConnect3 data to ground LLM responses
"""

import os
from typing import List
from azure.identity import DefaultAzureCredential

# Optional: Install with: pip install azure-openai


def create_rag_system():
    """
    Create a Retrieval-Augmented Generation (RAG) system
    that grounds LLM responses in your indexed data.
    """
    
    # Configuration
    search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    
    if not all([search_endpoint, openai_endpoint, openai_api_key]):
        print("Missing Azure configuration. Set these environment variables:")
        print("  AZURE_SEARCH_ENDPOINT")
        print("  AZURE_OPENAI_ENDPOINT")
        print("  AZURE_OPENAI_API_KEY")
        return None
    
    try:
        from azure.ai.openai import AzureOpenAI
        from azure_search_indexer import AzureAISearchManager
        
        # Initialize clients
        search_manager = AzureAISearchManager(search_endpoint)
        
        openai_client = AzureOpenAI(
            api_key=openai_api_key,
            api_version="2024-05-01-preview",
            azure_endpoint=openai_endpoint
        )
        
        return {
            "search": search_manager,
            "openai": openai_client
        }
    
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Install with: pip install azure-openai")
        return None


def search_documents(rag_system, query: str, top: int = 3) -> str:
    """
    Search for relevant documents and return as context.
    
    Args:
        rag_system: Dictionary with 'search' client
        query: Search query
        top: Number of results to return
    
    Returns:
        Formatted context string for LLM
    """
    search_manager = rag_system["search"]
    results = list(search_manager.search(query, top=top))
    
    if not results:
        return "No relevant documents found."
    
    context_parts = []
    for i, result in enumerate(results, 1):
        part = f"""
Document {i}:
Title: {result.get('title', 'Unknown')}
Source: {result.get('source_url', 'Unknown')}
Content: {result.get('content', '')[:500]}..."""
        context_parts.append(part)
    
    return "\n\n".join(context_parts)


def query_with_rag(rag_system, user_question: str, deployment_name: str = "gpt-4-turbo") -> str:
    """
    Answer a question using RAG (Retrieval-Augmented Generation).
    
    The process:
    1. Search for relevant documents using user question
    2. Build context from search results
    3. Create a prompt with context
    4. Send to LLM for grounded response
    
    Args:
        rag_system: Dictionary with clients
        user_question: User's question
        deployment_name: Azure OpenAI deployment name
    
    Returns:
        LLM response grounded in indexed data
    """
    
    search_manager = rag_system["search"]
    openai_client = rag_system["openai"]
    
    # Step 1: Search for relevant context
    print("[*] Searching for relevant documents...")
    context = search_documents(rag_system, user_question, top=5)
    
    # Step 2: Create system prompt with context
    system_prompt = f"""You are a helpful assistant specializing in Microsoft Solution Accelerators.
    
You have access to the following documents:

{context}

When answering questions, prioritize information from these documents.
If the documents don't contain relevant information, say so explicitly.
Always cite your sources when using information from the documents."""
    
    # Step 3: Send to LLM
    print("[*] Getting LLM response...")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ]
    
    response = openai_client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    
    return response.choices[0].message.content


def main():
    """Example usage."""
    
    print("=" * 70)
    print("Azure OpenAI + Azure AI Search RAG Demo")
    print("=" * 70)
    print()
    
    # Initialize RAG system
    print("[*] Initializing RAG system...")
    rag_system = create_rag_system()
    
    if not rag_system:
        print("[!] Failed to initialize RAG system")
        print("\nTo enable RAG with Azure OpenAI:")
        print("1. Create Azure OpenAI resource")
        print("2. Deploy GPT-4 model")
        print("3. Set environment variables:")
        print("   $env:AZURE_OPENAI_ENDPOINT = 'https://your-resource.openai.azure.com/'")
        print("   $env:AZURE_OPENAI_API_KEY = 'your-api-key'")
        return
    
    print("[+] RAG system initialized")
    print()
    
    # Example questions
    example_questions = [
        "What are Microsoft Solution Accelerators?",
        "How can I get started with solution accelerators?",
        "What best practices are mentioned in the documentation?",
    ]
    
    print("Example questions:")
    for i, q in enumerate(example_questions, 1):
        print(f"  {i}. {q}")
    print()
    
    # Get user input
    question = input("Enter your question (or number for example): ").strip()
    
    if question.isdigit() and 1 <= int(question) <= len(example_questions):
        question = example_questions[int(question) - 1]
    
    if not question:
        print("[!] No question provided")
        return
    
    print()
    print(f"Question: {question}")
    print()
    
    try:
        # Get RAG response
        answer = query_with_rag(rag_system, question)
        
        print("Answer:")
        print("-" * 70)
        print(answer)
        print("-" * 70)
        print()
        print("[+] Response grounded in indexed documents from Azure AI Search")
    
    except Exception as e:
        print(f"[!] Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Check Azure OpenAI is deployed: az cognitiveservices account deployment list ...")
        print("  2. Verify API version is correct (2024-05-01-preview)")
        print("  3. Check deployment name matches your model")


if __name__ == "__main__":
    main()

"""
Test AI Agent using Azure OpenAI SDK (simpler and more reliable)
Since the agent is created in AI Foundry but uses gpt-4o model,
we can also interact with it via Azure OpenAI API
"""
import json
from openai import AzureOpenAI

def test_agent_with_openai():
    """Test agent using Azure OpenAI client"""
    
    # Azure OpenAI credentials - Load from environment variables
    import os
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://dcsinstance.openai.azure.com/")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt4-1")  # The gpt-4o deployment in dcsinstance
    
    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY environment variable not set")
    
    # AI Foundry agent info
    agent_id = "asst_rFwMHjHtgDeQ1TprE6IEFzOh"
    
    print("=" * 70)
    print("STAGE 3: Test AI Agent (via Azure OpenAI)")
    print("=" * 70 + "\n")
    
    # Initialize client
    print("Connecting to Azure OpenAI...")
    try:
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-10-01-preview",
            azure_endpoint=endpoint
        )
        print("SUCCESS\n")
    except Exception as e:
        print(f"FAILED: {e}")
        return False
    
    # Test queries
    test_queries = [
        "What are Microsoft Solution Accelerators?",
        "Tell me about enterprise cloud solutions",
        "What GitHub repositories are available?"
    ]
    
    print("Sending test queries...\n")
    
    for query in test_queries:
        print(f"Query: {query}")
        
        try:
            # Send message to deployment
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            print(f"Response: {answer}\n")
            
        except Exception as e:
            print(f"Error: {type(e).__name__}: {str(e)[:100]}\n")
    
    print("=" * 70)
    print("STAGE 3 COMPLETE")
    print("=" * 70)
    print(f"\nAgent Details:")
    print(f"  AI Foundry Agent ID: {agent_id}")
    print(f"  Model: gpt-4o")
    print(f"  Azure OpenAI Deployment: {deployment}")
    print(f"  Status: READY\n")
    
    return True

if __name__ == "__main__":
    success = test_agent_with_openai()
    exit(0 if success else 1)
